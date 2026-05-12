from .base_parser import BaseParser
from typing import List, Dict, Any

class RadonParser(BaseParser):
    def parse(self, raw_output: Dict[str, Any]) -> List[Dict[str, Any]]:
        findings = []
        # cc_data = raw_output.get("cc", {})
        # mi_data = raw_output.get("mi", {})
        
        # Example for CC
        for file_path, blocks in raw_output.get("cc", {}).items():
            for block in blocks:
                complexity = block.get("complexity", 0)
                if complexity > 10:
                    findings.append({
                        "scanner": "radon",
                        "severity": "high" if complexity > 20 else "medium",
                        "category": "complexity",
                        "title": f"High Complexity in {block.get('name')}",
                        "description": f"Function '{block.get('name')}' has a cyclomatic complexity of {complexity}.",
                        "file_path": file_path,
                        "line_number": block.get("lineno"),
                        "rule_id": "radon-cc",
                        "remediation": "Consider refactoring this function to reduce complexity.",
                        "confidence": "high"
                    })
        return findings
