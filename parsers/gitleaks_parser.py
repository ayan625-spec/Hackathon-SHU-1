from .base_parser import BaseParser
from typing import List, Dict, Any

class GitLeaksParser(BaseParser):
    def parse(self, raw_output: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        findings = []
        if not isinstance(raw_output, list):
            return findings
            
        for leak in raw_output:
            findings.append({
                "scanner": "gitleaks",
                "severity": "critical",
                "category": "secrets",
                "title": f"Secret Found: {leak.get('Description')}",
                "description": f"Potential leak of {leak.get('Description')} in {leak.get('File')}",
                "file_path": leak.get("File"),
                "line_number": leak.get("StartLine"),
                "rule_id": leak.get("RuleID"),
                "remediation": "Revoke the secret immediately and update your configuration to use environment variables.",
                "confidence": "high"
            })
        return findings
