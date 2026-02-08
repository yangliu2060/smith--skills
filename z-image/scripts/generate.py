#!/usr/bin/env python3
"""
Z-Image CLI - ModelScope 通义万相图片生成

Usage:
    python generate.py "一个程序员在深夜写代码"
    python generate.py "武侠少年" --style anime_shonen
    python generate.py "纳瓦尔的智慧" --auto-style
    python generate.py prompts.txt --batch --style neon_wisdom
    python generate.py --list-styles
    python generate.py "test prompt" --dry-run
"""

import argparse
import asyncio
import hashlib
import json
import os
import sys
import time
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Optional, List

# 确保能导入同目录的 style_templates
sys.path.insert(0, str(Path(__file__).parent))
from style_templates import (
    get_style_prompt, auto_detect_style, list_styles,
    list_styles_by_category, STYLES, DEFAULT_STYLE, StyleCategory
)


@dataclass
class Result:
    """生成结果"""
    success: bool
    image_path: Optional[str] = None
    prompt_used: str = ""
    style: str = ""
    error: Optional[str] = None

    def to_dict(self) -> dict:
        return asdict(self)


class ZImageClient:
    """Z-Image API 客户端"""

    BASE_URL = "https://api-inference.modelscope.cn/"
    DEFAULT_MODEL = "Tongyi-MAI/Z-Image-Turbo"
    POLL_INTERVAL = 5
    MAX_POLL_ATTEMPTS = 60

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or self._resolve_api_key()
        self._session = None

    def _resolve_api_key(self) -> str:
        """按优先级解析 API Key"""
        # 1. 环境变量
        key = os.environ.get("MODELSCOPE_API_KEY")
        if key:
            return key

        # 2. secrets.md 配置文件
        secrets_path = Path(__file__).parent.parent / "config" / "secrets.md"
        if secrets_path.exists():
            for line in secrets_path.read_text().splitlines():
                if line.startswith("API_KEY="):
                    return line.split("=", 1)[1].strip()

        # 3. 无 key
        return ""

    async def _get_session(self):
        if self._session is None or self._session.closed:
            import aiohttp
            self._session = aiohttp.ClientSession()
        return self._session

    async def generate(
        self,
        prompt: str,
        style: str = DEFAULT_STYLE,
        output_dir: Optional[Path] = None,
        size: str = "1024x1024",
    ) -> Result:
        """
        生成图片

        Args:
            prompt: 图片描述
            style: 风格 ID
            output_dir: 输出目录
            size: 输出尺寸 (WxH)

        Returns:
            Result 对象
        """
        import aiohttp

        if not self.api_key:
            return Result(success=False, error="未配置 API Key。请设置 MODELSCOPE_API_KEY 环境变量或 config/secrets.md")

        output_dir = output_dir or Path.cwd() / "output" / "z-image"
        output_dir.mkdir(parents=True, exist_ok=True)

        # 风格增强
        enhanced = get_style_prompt(prompt, style, include_negative=False)

        # 提交任务
        session = await self._get_session()
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "X-ModelScope-Async-Mode": "true",
        }
        payload = {
            "model": self.DEFAULT_MODEL,
            "prompt": enhanced,
        }

        try:
            async with session.post(
                f"{self.BASE_URL}v1/images/generations",
                headers=headers,
                data=json.dumps(payload, ensure_ascii=False).encode("utf-8")
            ) as resp:
                if resp.status != 200:
                    error_text = await resp.text()
                    return Result(success=False, prompt_used=enhanced, style=style,
                                  error=f"API 提交失败: {resp.status} - {error_text}")
                result = await resp.json()

            task_id = result.get("task_id")
            if not task_id:
                return Result(success=False, prompt_used=enhanced, style=style,
                              error=f"未返回 task_id: {result}")

            # 轮询
            image_url = await self._poll_task(task_id)

            # 下载
            image_path = await self._download_image(image_url, output_dir, size)

            return Result(
                success=True,
                image_path=str(image_path),
                prompt_used=enhanced,
                style=style,
            )

        except Exception as e:
            return Result(success=False, prompt_used=enhanced, style=style, error=str(e))

    async def _poll_task(self, task_id: str) -> str:
        """轮询任务状态"""
        session = await self._get_session()
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "X-ModelScope-Task-Type": "image_generation",
        }

        for attempt in range(self.MAX_POLL_ATTEMPTS):
            await asyncio.sleep(self.POLL_INTERVAL)
            async with session.get(
                f"{self.BASE_URL}v1/tasks/{task_id}",
                headers=headers
            ) as resp:
                if resp.status != 200:
                    continue
                data = await resp.json()
                status = data.get("task_status")

                if status == "SUCCEED":
                    images = data.get("output_images", [])
                    if images:
                        return images[0]
                    raise Exception("API 成功但无图片返回")
                elif status == "FAILED":
                    raise Exception(f"生成失败: {data.get('error', '未知错误')}")

        raise Exception(f"超时: 任务 {task_id} 未在 {self.MAX_POLL_ATTEMPTS * self.POLL_INTERVAL}s 内完成")

    async def _download_image(self, url: str, output_dir: Path, size: str) -> Path:
        """下载图片"""
        session = await self._get_session()
        async with session.get(url) as resp:
            if resp.status != 200:
                raise Exception(f"下载失败: {resp.status}")
            image_data = await resp.read()

        # 尝试用 PIL 调整尺寸
        try:
            from PIL import Image
            from io import BytesIO
            image = Image.open(BytesIO(image_data))
            w, h = [int(x) for x in size.split("x")]
            image = image.resize((w, h), Image.Resampling.LANCZOS)
            filename = f"zimg_{int(time.time())}_{hashlib.md5(url.encode()).hexdigest()[:6]}.png"
            output_path = output_dir / filename
            image.save(output_path)
        except ImportError:
            # 无 PIL 则直接保存原始数据
            filename = f"zimg_{int(time.time())}_{hashlib.md5(url.encode()).hexdigest()[:6]}.png"
            output_path = output_dir / filename
            output_path.write_bytes(image_data)

        return output_path

    async def close(self):
        if self._session and not self._session.closed:
            await self._session.close()


def cmd_list_styles(category: Optional[str] = None):
    """列出风格"""
    if category:
        styles = list_styles_by_category(category)
        if not styles:
            print(f"未知分类: {category}")
            print(f"可用分类: {', '.join(c.value for c in StyleCategory)}")
            sys.exit(11)
        print(f"\n[{category}] ({len(styles)} styles)")
        for s in styles:
            print(f"  {s['id']:20s} {s['name']:8s} - {s['description']}")
    else:
        all_styles = list_styles()
        current_cat = None
        print(f"\nZ-Image 风格模板 ({len(all_styles)} styles)\n{'='*60}")
        for s in all_styles:
            if s['category'] != current_cat:
                current_cat = s['category']
                print(f"\n[{current_cat}]")
            print(f"  {s['id']:20s} {s['name']:8s} - {s['description']}")
    print()


def cmd_dry_run(prompt: str, style: str, auto: bool):
    """Dry run - 只输出增强后的 prompt"""
    if auto:
        style = auto_detect_style(prompt)
        print(f"Auto-detected style: {style}")

    enhanced = get_style_prompt(prompt, style, include_negative=True)
    parts = enhanced.split(" ||| ")
    print(f"\nStyle: {style} ({STYLES[style].name})")
    print(f"\n[Positive Prompt]\n{parts[0]}")
    if len(parts) > 1:
        print(f"\n[Negative Prompt]\n{parts[1]}")
    print()


async def cmd_generate(prompt: str, style: str, auto: bool, output_dir: Optional[str],
                       size: str, api_key: Optional[str]):
    """生成图片"""
    if auto:
        style = auto_detect_style(prompt)
        print(f"Auto-detected style: {style} ({STYLES[style].name})")

    print(f"Generating with style: {style}")
    print(f"Prompt: {prompt[:80]}{'...' if len(prompt) > 80 else ''}")

    client = ZImageClient(api_key=api_key)
    out = Path(output_dir) if output_dir else None

    try:
        result = await client.generate(prompt, style=style, output_dir=out, size=size)
        if result.success:
            print(f"\nSuccess! Image saved to: {result.image_path}")
        else:
            print(f"\nFailed: {result.error}", file=sys.stderr)
            sys.exit(10)
    finally:
        await client.close()


async def cmd_batch(file_path: str, style: str, output_dir: Optional[str],
                    size: str, api_key: Optional[str]):
    """批量生成"""
    prompts = Path(file_path).read_text(encoding="utf-8").strip().splitlines()
    prompts = [p.strip() for p in prompts if p.strip() and not p.startswith("#")]

    print(f"Batch mode: {len(prompts)} prompts, style: {style}")

    client = ZImageClient(api_key=api_key)
    out = Path(output_dir) if output_dir else None
    results = []

    try:
        for i, prompt in enumerate(prompts, 1):
            print(f"\n[{i}/{len(prompts)}] {prompt[:60]}...")
            result = await client.generate(prompt, style=style, output_dir=out, size=size)
            results.append(result)
            if result.success:
                print(f"  -> {result.image_path}")
            else:
                print(f"  -> FAILED: {result.error}")
    finally:
        await client.close()

    success = sum(1 for r in results if r.success)
    print(f"\n{'='*40}")
    print(f"Batch complete: {success}/{len(results)} succeeded")

    if success < len(results):
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Z-Image CLI - ModelScope 通义万相图片生成",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s "一个程序员在深夜写代码"
  %(prog)s "武侠少年仗剑天涯" --style anime_shonen
  %(prog)s "纳瓦尔的智慧哲学" --auto-style
  %(prog)s prompts.txt --batch --style neon_wisdom
  %(prog)s --list-styles
  %(prog)s --list-styles --category anime
  %(prog)s "test" --dry-run
        """
    )

    parser.add_argument("prompt", nargs="?", help="图片描述 prompt 或批量文件路径")
    parser.add_argument("--style", "-s", default=DEFAULT_STYLE, help=f"风格 ID (default: {DEFAULT_STYLE})")
    parser.add_argument("--auto-style", "-a", action="store_true", help="自动检测风格")
    parser.add_argument("--batch", "-b", action="store_true", help="批量模式（prompt 参数为文件路径）")
    parser.add_argument("--output", "-o", help="输出目录")
    parser.add_argument("--size", default="1024x1024", help="输出尺寸 WxH (default: 1024x1024)")
    parser.add_argument("--api-key", help="ModelScope API Key")
    parser.add_argument("--list-styles", action="store_true", help="列出所有风格")
    parser.add_argument("--category", help="按分类筛选风格 (配合 --list-styles)")
    parser.add_argument("--dry-run", action="store_true", help="只输出增强后的 prompt，不调用 API")
    parser.add_argument("--json", action="store_true", help="JSON 格式输出")

    args = parser.parse_args()

    # 列出风格
    if args.list_styles:
        cmd_list_styles(args.category)
        sys.exit(0)

    # 需要 prompt
    if not args.prompt:
        parser.print_help()
        sys.exit(1)

    # Dry run
    if args.dry_run:
        cmd_dry_run(args.prompt, args.style, args.auto_style)
        sys.exit(0)

    # 批量模式
    if args.batch:
        asyncio.run(cmd_batch(args.prompt, args.style, args.output, args.size, args.api_key))
    else:
        asyncio.run(cmd_generate(args.prompt, args.style, args.auto_style, args.output, args.size, args.api_key))


if __name__ == "__main__":
    main()
