"""
JSON 报告生成器
"""

import json
from datetime import datetime
from typing import List, Dict, Any
from ..scoring import SkillAuditResult, RiskLevel


class JSONReporter:
    """JSON 报告生成器"""

    def __init__(self):
        self.version = "1.0.0"

    def generate_report(self, results: List[SkillAuditResult], scan_time: float) -> Dict[str, Any]:
        """生成 JSON 报告"""
        report = {
            "version": self.version,
            "generated_at": datetime.now().isoformat(),
            "scan_time_seconds": round(scan_time, 2),
            "summary": self._generate_summary(results),
            "skills": [self._serialize_result(r) for r in results]
        }
        return report

    def _generate_summary(self, results: List[SkillAuditResult]) -> Dict[str, Any]:
        """生成摘要"""
        level_counts = {level.value: 0 for level in RiskLevel}
        total_findings = 0

        for r in results:
            level_counts[r.risk_level.value] += 1
            total_findings += len(r.findings)

        return {
            "total_skills": len(results),
            "total_findings": total_findings,
            "by_risk_level": level_counts
        }

    def _serialize_result(self, result: SkillAuditResult) -> Dict[str, Any]:
        """序列化单个结果"""
        return {
            "name": result.skill_name,
            "path": result.skill_path,
            "risk_level": result.risk_level.value,
            "total_score": result.total_score,
            "has_hard_trigger": result.has_hard_trigger,
            "file_count": result.file_count,
            "script_count": result.script_count,
            "allowed_tools": result.allowed_tools,
            "allowed_tools_parsed": result.allowed_tools_parsed,
            "findings": [
                {
                    "rule_id": f.rule_id,
                    "rule_name": f.rule_name,
                    "severity": f.severity.value,
                    "category": f.category.value,
                    "file": f.file_path,
                    "line": f.line_number,
                    "snippet": f.snippet,
                    "weight": f.weight,
                    "hard_trigger": f.hard_trigger
                }
                for f in result.findings
            ]
        }

    def to_json_string(self, results: List[SkillAuditResult], scan_time: float, indent: int = 2) -> str:
        """生成 JSON 字符串"""
        report = self.generate_report(results, scan_time)
        return json.dumps(report, ensure_ascii=False, indent=indent)

    def save_to_file(self, results: List[SkillAuditResult], scan_time: float, file_path: str):
        """保存到文件"""
        json_str = self.to_json_string(results, scan_time)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(json_str)
