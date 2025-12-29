"""
风险评分引擎

基于三大战神设计的评分算法:
- 规则分 + 权限面分 + 不一致分 + 硬触发
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional
from enum import Enum
from pathlib import Path

from .detectors.patterns import PatternRule, Severity, Category, get_all_patterns


class RiskLevel(Enum):
    """风险等级"""
    SAFE = "safe"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    DANGEROUS = "dangerous"


# 严重程度权重
SEVERITY_WEIGHTS: Dict[Severity, int] = {
    Severity.LOW: 3,
    Severity.MEDIUM: 10,
    Severity.HIGH: 20,
    Severity.CRITICAL: 40,
}

# 风险等级阈值
RISK_THRESHOLDS = {
    RiskLevel.LOW: 1,
    RiskLevel.MEDIUM: 25,
    RiskLevel.HIGH: 50,
    RiskLevel.DANGEROUS: 75,
}


@dataclass
class Finding:
    """单个发现"""
    rule_id: str
    rule_name: str
    severity: Severity
    category: Category
    file_path: str
    line_number: int
    snippet: str
    weight: int
    hard_trigger: bool = False


@dataclass
class SkillAuditResult:
    """Skill 审计结果"""
    skill_name: str
    skill_path: str
    findings: List[Finding] = field(default_factory=list)
    allowed_tools: List[str] = field(default_factory=list)
    allowed_tools_parsed: bool = False
    total_score: int = 0
    risk_level: RiskLevel = RiskLevel.SAFE
    has_hard_trigger: bool = False
    file_count: int = 0
    script_count: int = 0


def scan_content(content: str, file_path: str, is_script: bool = True) -> List[Finding]:
    """扫描内容，检测危险模式"""
    findings: List[Finding] = []
    lines = content.split('\n')
    patterns = get_all_patterns()

    for rule in patterns:
        for line_num, line in enumerate(lines, 1):
            match = rule.pattern.search(line)
            if match:
                # 对 .md 文件降低权重（可能是文档示例）
                weight = rule.weight
                if file_path.endswith('.md') and not is_script:
                    weight = int(weight * 0.5)

                # 截取 snippet
                snippet = line.strip()[:100]
                if len(line.strip()) > 100:
                    snippet += '...'

                finding = Finding(
                    rule_id=rule.id,
                    rule_name=rule.name,
                    severity=rule.severity,
                    category=rule.category,
                    file_path=file_path,
                    line_number=line_num,
                    snippet=snippet,
                    weight=weight,
                    hard_trigger=rule.hard_trigger
                )
                findings.append(finding)

    return findings


def calculate_score(findings: List[Finding]) -> tuple:
    """
    计算风险分数

    Returns:
        (total_score, risk_level, has_hard_trigger)
    """
    if not findings:
        return 0, RiskLevel.SAFE, False

    # 检查硬触发
    has_hard_trigger = any(f.hard_trigger for f in findings)

    # 计算总分（同类规则衰减）
    rule_counts: Dict[str, int] = {}
    total = 0

    for f in findings:
        rule_counts[f.rule_id] = rule_counts.get(f.rule_id, 0) + 1
        count = rule_counts[f.rule_id]

        # 首次全额，重复 50%
        multiplier = 1.0 if count == 1 else 0.5
        total += int(f.weight * multiplier)

    # 硬触发加权
    if has_hard_trigger:
        total = max(total, 75)  # 至少 75 分

    # 限制最大分数
    total = min(total, 100)

    # 确定风险等级
    if has_hard_trigger or total >= RISK_THRESHOLDS[RiskLevel.DANGEROUS]:
        risk_level = RiskLevel.DANGEROUS
    elif total >= RISK_THRESHOLDS[RiskLevel.HIGH]:
        risk_level = RiskLevel.HIGH
    elif total >= RISK_THRESHOLDS[RiskLevel.MEDIUM]:
        risk_level = RiskLevel.MEDIUM
    elif total >= RISK_THRESHOLDS[RiskLevel.LOW]:
        risk_level = RiskLevel.LOW
    else:
        risk_level = RiskLevel.SAFE

    return total, risk_level, has_hard_trigger


def audit_skill(skill_info, skill_md_info: Optional[dict] = None) -> SkillAuditResult:
    """审计单个 Skill"""
    from .scanner import SkillInfo

    result = SkillAuditResult(
        skill_name=skill_info.name,
        skill_path=str(skill_info.path),
        file_count=len(skill_info.files),
        script_count=sum(1 for f in skill_info.files if f.is_script)
    )

    # 解析 allowed-tools
    if skill_md_info:
        result.allowed_tools = skill_md_info.get('allowed_tools', [])
        result.allowed_tools_parsed = skill_md_info.get('parse_success', False)

    # 扫描所有文件
    all_findings: List[Finding] = []

    for scanned_file in skill_info.files:
        try:
            content = scanned_file.path.read_text(encoding='utf-8', errors='ignore')
            file_findings = scan_content(
                content,
                str(scanned_file.relative_path),
                scanned_file.is_script
            )
            all_findings.extend(file_findings)
        except Exception:
            continue

    result.findings = all_findings

    # 计算分数
    score, level, hard_trigger = calculate_score(all_findings)
    result.total_score = score
    result.risk_level = level
    result.has_hard_trigger = hard_trigger

    return result
