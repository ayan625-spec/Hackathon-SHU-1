from .base_parser import BaseParser
from typing import List, Dict, Any

class SemgrepParser(BaseParser):
    def parse(self, raw_output: Dict[str, Any]) -> List[Dict[str, Any]]:
        findings = []
        for result in raw_output.get("results", []):
            extra = result.get("extra", {})
            findings.append({
                "scanner": "semgrep",
                "severity": extra.get("severity", "low").lower(),
                "category": "security",
                "title": extra.get("message", "Semgrep Finding").split('\n')[0],
                "description": extra.get("message", ""),
                "file_path": result.get("path"),
                "line_number": result.get("start", {}).get("line"),
                "rule_id": result.get("check_id"),
                "remediation": extra.get("metadata", {}).get("remediation_guidance"),
                "confidence": "high" if extra.get("metadata", {}).get("confidence") == "HIGH" else "medium"
            })
        return findings
