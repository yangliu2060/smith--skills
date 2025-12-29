#!/usr/bin/env python3
"""
Skill Auditor - Claude Skills 安全审计工具

使用方法:
    python3 -m skill_auditor [OPTIONS]

示例:
    python3 -m skill_auditor                    # 扫描默认目录
    python3 -m skill_auditor --json             # JSON 输出
    python3 -m skill_auditor --output report.json
    python3 -m skill_auditor --min-level high   # 仅显示高风险
"""

import argparse
import sys
import time
from pathlib import Path
from typing import List, Optional

from .scanner import scan_skills_root, get_default_skills_root
from .parsers.skill_md import parse_skill_md
from .scoring import audit_skill, SkillAuditResult, RiskLevel
from .reporters.terminal import TerminalReporter
from .reporters.json_report import JSONReporter


def parse_args() -> argparse.Namespace:
    """解析命令行参数"""
    parser = argparse.ArgumentParser(
        prog='skill-auditor',
        description='Claude Skills 安全审计工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
示例:
  python3 -m skill_auditor                    # 扫描 ~/.claude/skills/
  python3 -m skill_auditor --json             # JSON 格式输出
  python3 -m skill_auditor -o report.json     # 保存报告
  python3 -m skill_auditor --min-level high   # 仅显示高风险
  python3 -m skill_auditor --verbose          # 详细模式
'''
    )

    parser.add_argument(
        '--root', '-r',
        type=str,
        default=None,
        help='Skills 根目录 (默认: ~/.claude/skills)'
    )

    parser.add_argument(
        '--json', '-j',
        action='store_true',
        help='输出 JSON 格式'
    )

    parser.add_argument(
        '--output', '-o',
        type=str,
        default=None,
        help='输出文件路径'
    )

    parser.add_argument(
        '--min-level', '-m',
        type=str,
        choices=['safe', 'low', 'medium', 'high', 'dangerous'],
        default='safe',
        help='最低显示风险等级 (默认: safe)'
    )

    parser.add_argument(
        '--no-color',
        action='store_true',
        help='禁用彩色输出'
    )

    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='详细模式，显示所有发现'
    )

    parser.add_argument(
        '--version',
        action='version',
        version='skill-auditor 1.0.0'
    )

    return parser.parse_args()


def filter_by_level(results: List[SkillAuditResult], min_level: str) -> List[SkillAuditResult]:
    """按风险等级过滤"""
    level_order = ['safe', 'low', 'medium', 'high', 'dangerous']
    min_index = level_order.index(min_level)

    return [
        r for r in results
        if level_order.index(r.risk_level.value) >= min_index
    ]


def main():
    """主函数"""
    args = parse_args()

    # 确定扫描目录
    if args.root:
        root_path = Path(args.root).expanduser()
    else:
        root_path = get_default_skills_root()

    if not root_path.exists():
        print(f"错误: 目录不存在: {root_path}", file=sys.stderr)
        sys.exit(1)

    # 开始扫描
    start_time = time.time()

    print(f"扫描目录: {root_path}", file=sys.stderr)

    # 扫描所有 skills
    skills = scan_skills_root(root_path)

    if not skills:
        print("未找到任何 skill", file=sys.stderr)
        sys.exit(0)

    print(f"发现 {len(skills)} 个 skills，正在分析...", file=sys.stderr)

    # 审计每个 skill
    results: List[SkillAuditResult] = []

    for skill_info in skills:
        # 解析 skill.md
        skill_md_info = None
        if skill_info.skill_md_path:
            parsed = parse_skill_md(skill_info.skill_md_path)
            skill_md_info = {
                'allowed_tools': parsed.allowed_tools,
                'parse_success': parsed.parse_success
            }

        # 审计
        result = audit_skill(skill_info, skill_md_info)
        results.append(result)

    scan_time = time.time() - start_time

    # 过滤结果
    filtered_results = filter_by_level(results, args.min_level)

    # 生成报告
    if args.json:
        reporter = JSONReporter()
        if args.output:
            reporter.save_to_file(filtered_results, scan_time, args.output)
            print(f"报告已保存至: {args.output}", file=sys.stderr)
        else:
            print(reporter.to_json_string(filtered_results, scan_time))
    else:
        reporter = TerminalReporter(
            use_color=not args.no_color,
            verbose=args.verbose
        )

        if args.output:
            # 保存纯文本报告
            report = reporter.generate_report(filtered_results, scan_time)
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(report)
            print(f"报告已保存至: {args.output}", file=sys.stderr)
        else:
            reporter.print_report(filtered_results, scan_time)

    # 返回码：有危险级别时返回非零
    dangerous_count = sum(1 for r in results if r.risk_level == RiskLevel.DANGEROUS)
    if dangerous_count > 0:
        sys.exit(1)


if __name__ == '__main__':
    main()
