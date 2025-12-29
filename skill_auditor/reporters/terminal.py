"""
终端彩色报告生成器
"""

import sys
from typing import List
from ..scoring import SkillAuditResult, RiskLevel, Finding, Severity


# ANSI 颜色码
class Colors:
    RESET = '\033[0m'
    BOLD = '\033[1m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    ORANGE = '\033[38;5;208m'


# 风险等级颜色和图标
RISK_COLORS = {
    RiskLevel.SAFE: (Colors.GREEN, '🟢'),
    RiskLevel.LOW: (Colors.BLUE, '🔵'),
    RiskLevel.MEDIUM: (Colors.YELLOW, '🟡'),
    RiskLevel.HIGH: (Colors.ORANGE, '🟠'),
    RiskLevel.DANGEROUS: (Colors.RED, '🔴'),
}

# 严重程度颜色
SEVERITY_COLORS = {
    Severity.LOW: Colors.BLUE,
    Severity.MEDIUM: Colors.YELLOW,
    Severity.HIGH: Colors.ORANGE,
    Severity.CRITICAL: Colors.RED,
}


class TerminalReporter:
    """终端报告生成器"""

    def __init__(self, use_color: bool = True, verbose: bool = False):
        self.use_color = use_color and sys.stdout.isatty()
        self.verbose = verbose

    def _color(self, text: str, color: str) -> str:
        """添加颜色"""
        if self.use_color:
            return f"{color}{text}{Colors.RESET}"
        return text

    def _bold(self, text: str) -> str:
        """加粗"""
        if self.use_color:
            return f"{Colors.BOLD}{text}{Colors.RESET}"
        return text

    def generate_report(self, results: List[SkillAuditResult], scan_time: float) -> str:
        """生成完整报告"""
        lines: List[str] = []

        # 标题
        lines.append('')
        lines.append(self._bold('╔══════════════════════════════════════════════════════════════╗'))
        lines.append(self._bold('║              Skill Security Audit Report                      ║'))
        lines.append(self._bold('╚══════════════════════════════════════════════════════════════╝'))
        lines.append('')

        # 统计
        total_skills = len(results)
        total_findings = sum(len(r.findings) for r in results)
        dangerous = sum(1 for r in results if r.risk_level == RiskLevel.DANGEROUS)
        high = sum(1 for r in results if r.risk_level == RiskLevel.HIGH)

        stats = f"Scanned: {total_skills} skills | Findings: {total_findings} | Time: {scan_time:.1f}s"
        if dangerous > 0:
            stats += f" | {self._color(f'DANGEROUS: {dangerous}', Colors.RED)}"
        if high > 0:
            stats += f" | {self._color(f'HIGH: {high}', Colors.ORANGE)}"

        lines.append(stats)
        lines.append('')

        # 按风险等级排序
        sorted_results = sorted(
            results,
            key=lambda r: (
                list(RiskLevel).index(r.risk_level) * -1,
                r.total_score * -1
            )
        )

        # 每个 skill 的结果
        for result in sorted_results:
            color, icon = RISK_COLORS[result.risk_level]

            # Skill 标题行
            level_name = result.risk_level.value.upper()
            skill_line = f"{icon} {self._color(level_name.ljust(10), color)} "
            skill_line += f"{self._bold(result.skill_name.ljust(25))} "
            skill_line += f"Score: {result.total_score}"

            if result.has_hard_trigger:
                skill_line += self._color(' [HARD TRIGGER]', Colors.RED)

            lines.append(skill_line)

            # 显示发现（最多 5 个）
            if result.findings:
                shown = result.findings[:5] if not self.verbose else result.findings

                for finding in shown:
                    sev_color = SEVERITY_COLORS[finding.severity]
                    sev_name = finding.severity.value.upper()

                    finding_line = f"   └─ [{self._color(sev_name, sev_color)}] "
                    finding_line += f"{finding.rule_name} at {finding.file_path}:{finding.line_number}"

                    lines.append(finding_line)

                    if self.verbose:
                        lines.append(f"      {self._color(finding.snippet, Colors.CYAN)}")

                if len(result.findings) > 5 and not self.verbose:
                    lines.append(f"   └─ ... and {len(result.findings) - 5} more findings")

            lines.append('')

        return '\n'.join(lines)

    def print_report(self, results: List[SkillAuditResult], scan_time: float):
        """打印报告到终端"""
        report = self.generate_report(results, scan_time)
        print(report)
