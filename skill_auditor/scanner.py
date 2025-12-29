"""
文件扫描器

扫描 skills 目录，收集待审计文件
"""

import os
from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Optional, Set

# 跳过的目录
SKIP_DIRS: Set[str] = {
    '.git', 'node_modules', '__pycache__', '.venv', 'venv',
    'dist', 'build', '.cache', '.pytest_cache', 'coverage'
}

# 脚本扩展名
SCRIPT_EXTENSIONS: Set[str] = {
    '.py', '.sh', '.bash', '.zsh', '.js', '.ts',
    '.rb', '.pl', '.ps1', '.cmd', '.bat'
}

# 最大文件大小 (2MB)
MAX_FILE_SIZE: int = 2 * 1024 * 1024


@dataclass
class ScannedFile:
    """扫描到的文件"""
    path: Path
    relative_path: str
    extension: str
    size: int
    is_script: bool
    has_shebang: bool = False


@dataclass
class SkillInfo:
    """Skill 信息"""
    name: str
    path: Path
    skill_md_path: Optional[Path]
    files: List[ScannedFile] = field(default_factory=list)
    allowed_tools: List[str] = field(default_factory=list)


def is_binary_file(file_path: Path) -> bool:
    """检测是否为二进制文件"""
    try:
        with open(file_path, 'rb') as f:
            chunk = f.read(8192)
            return b'\x00' in chunk
    except Exception:
        return True


def has_shebang(file_path: Path) -> bool:
    """检测是否有 shebang"""
    try:
        with open(file_path, 'rb') as f:
            first_line = f.readline()
            return first_line.startswith(b'#!')
    except Exception:
        return False


def find_skill_md(skill_dir: Path) -> Optional[Path]:
    """查找 skill.md 文件（大小写不敏感）"""
    for name in ['skill.md', 'SKILL.md', 'Skill.md']:
        path = skill_dir / name
        if path.exists():
            return path
    return None


def scan_skill_directory(skill_dir: Path) -> SkillInfo:
    """扫描单个 skill 目录"""
    skill_name = skill_dir.name
    skill_md_path = find_skill_md(skill_dir)

    skill_info = SkillInfo(
        name=skill_name,
        path=skill_dir,
        skill_md_path=skill_md_path
    )

    for root, dirs, files in os.walk(skill_dir):
        # 跳过特定目录
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]

        root_path = Path(root)

        for filename in files:
            file_path = root_path / filename

            # 跳过过大文件
            try:
                size = file_path.stat().st_size
                if size > MAX_FILE_SIZE:
                    continue
            except Exception:
                continue

            # 跳过二进制文件
            if is_binary_file(file_path):
                continue

            ext = file_path.suffix.lower()
            is_script = ext in SCRIPT_EXTENSIONS

            # 检查 shebang
            file_has_shebang = False
            if not is_script:
                file_has_shebang = has_shebang(file_path)
                if file_has_shebang:
                    is_script = True

            relative = file_path.relative_to(skill_dir)

            scanned = ScannedFile(
                path=file_path,
                relative_path=str(relative),
                extension=ext,
                size=size,
                is_script=is_script,
                has_shebang=file_has_shebang
            )

            skill_info.files.append(scanned)

    return skill_info


def scan_skills_root(root_path: Path) -> List[SkillInfo]:
    """扫描 skills 根目录"""
    skills: List[SkillInfo] = []

    if not root_path.exists():
        return skills

    for entry in root_path.iterdir():
        if not entry.is_dir():
            continue

        # 跳过隐藏目录
        if entry.name.startswith('.'):
            continue

        # 检查是否是有效的 skill 目录
        skill_md = find_skill_md(entry)
        if skill_md or any((entry / f).exists() for f in ['scripts', '__main__.py']):
            skill_info = scan_skill_directory(entry)
            skills.append(skill_info)

    return skills


def get_default_skills_root() -> Path:
    """获取默认的 skills 根目录"""
    return Path.home() / '.claude' / 'skills'
