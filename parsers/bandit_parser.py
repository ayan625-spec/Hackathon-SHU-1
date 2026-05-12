from .base_parser import BaseParser
from typing import List, Dict, Any

class BanditParser(BaseParser):
    def parse(self, raw_output: Dict[str, Any]) -> List[Dict[str, Any]]:
        findings = []
        for issue in raw_output.get("results", []):
            findings.append({
                "scanner": "bandit",
                "severity": issue.get("issue_severity", "low").lower(),
                "category": "security",
                "title": issue.get("issue_text"),
                "description": f"Bandit detected a potential security issue: {issue.get('issue_text')}",
                "file_path": issue.get("filename"),
                "line_number": issue.get("line_number"),
                "rule_id": issue.get("test_id"),
                "remediation": f"Refactor code at line {issue.get('line_number')} to address {issue.get('test_name')}",
                "confidence": issue.get("issue_confidence", "low").lower()
            })
        return findings
