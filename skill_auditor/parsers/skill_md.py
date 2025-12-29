"""
skill.md 解析器

解析 skill.md 中的 allowed-tools 声明
"""

import re
from pathlib import Path
from typing import List, Optional, Tuple
from dataclasses import dataclass


@dataclass
class SkillMdInfo:
    """skill.md 解析结果"""
    allowed_tools: List[str]
    parse_success: bool
    raw_section: Optional[str] = None
    error: Optional[str] = None


def extract_allowed_tools(content: str) -> Tuple[List[str], bool, Optional[str]]:
    """
    从 skill.md 内容中提取 allowed-tools

    支持多种格式:
    1. allowed-tools: Tool1, Tool2, Tool3
    2. allowed-tools: Tool1(pattern), Tool2
    3. YAML front-matter 中的 allowed_tools

    Returns:
        (tools_list, success, raw_section)
    """
    tools: List[str] = []

    # 格式 1: 行末 allowed-tools: xxx
    pattern1 = re.compile(r'allowed[_-]?tools\s*:\s*(.+?)$', re.IGNORECASE | re.MULTILINE)
    match1 = pattern1.search(content)

    if match1:
        raw = match1.group(1).strip()
        # 解析逗号分隔的工具列表
        # 支持 Tool(pattern) 格式
        tool_pattern = re.compile(r'([A-Za-z_][A-Za-z0-9_]*(?:\([^)]*\))?)')
        tools = tool_pattern.findall(raw)
        if tools:
            return tools, True, raw

    # 格式 2: YAML front-matter
    yaml_pattern = re.compile(r'^---\s*\n(.*?)\n---', re.DOTALL)
    yaml_match = yaml_pattern.search(content)

    if yaml_match:
        yaml_content = yaml_match.group(1)
        # 简单解析 allowed_tools/allowed-tools
        tools_line = re.search(r'allowed[_-]?tools\s*:\s*\[([^\]]+)\]', yaml_content, re.I)
        if tools_line:
            raw = tools_line.group(1)
            tools = [t.strip().strip('"\'') for t in raw.split(',')]
            if tools:
                return tools, True, raw

        # 列表格式
        tools_section = re.search(r'allowed[_-]?tools\s*:\s*\n((?:\s+-\s+.+\n?)+)', yaml_content, re.I)
        if tools_section:
            raw = tools_section.group(0)
            items = re.findall(r'-\s+(.+)', tools_section.group(1))
            tools = [t.strip().strip('"\'') for t in items]
            if tools:
                return tools, True, raw

    # 格式 3: Markdown 列表在 allowed-tools 标题下
    section_pattern = re.compile(
        r'#+\s*allowed[_-]?tools\s*\n((?:[*-]\s+.+\n?)+)',
        re.IGNORECASE
    )
    section_match = section_pattern.search(content)

    if section_match:
        raw = section_match.group(0)
        items = re.findall(r'[*-]\s+(.+)', section_match.group(1))
        tools = [t.strip().strip('`"\'') for t in items]
        if tools:
            return tools, True, raw

    return [], False, None


def parse_skill_md(file_path: Path) -> SkillMdInfo:
    """解析 skill.md 文件"""
    try:
        content = file_path.read_text(encoding='utf-8')
        tools, success, raw = extract_allowed_tools(content)

        return SkillMdInfo(
            allowed_tools=tools,
            parse_success=success,
            raw_section=raw
        )
    except Exception as e:
        return SkillMdInfo(
            allowed_tools=[],
            parse_success=False,
            error=str(e)
        )


def infer_required_permissions(content: str) -> List[str]:
    """
    从代码内容推断所需权限

    用于检测代码行为是否超出 allowed-tools 声明
    """
    required: List[str] = []

    # 检测网络请求
    network_patterns = [
        r'urllib\.request',
        r'http\.client',
        r'requests\.',
        r'\bcurl\b',
        r'\bwget\b',
    ]
    for pattern in network_patterns:
        if re.search(pattern, content, re.I):
            required.append('network')
            break

    # 检测 Shell 执行
    shell_patterns = [
        r'subprocess\.',
        r'os\.system',
        r'os\.popen',
        r'\beval\b',
        r'\bexec\b',
    ]
    for pattern in shell_patterns:
        if re.search(pattern, content):
            required.append('shell')
            break

    # 检测文件写入
    write_patterns = [
        r'open\s*\([^)]*["\']w',
        r'\.write\s*\(',
        r'>\s*["\'/~]',
        r'>>\s*["\'/~]',
    ]
    for pattern in write_patterns:
        if re.search(pattern, content, re.I):
            required.append('filesystem_write')
            break

    return required
