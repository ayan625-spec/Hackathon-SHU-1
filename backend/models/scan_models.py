from pydantic import BaseModel
from typing import Optional, List

class ScanRequest(BaseModel):
    repo_url: str
    user_id: str = "guest"

class Finding(BaseModel):
    scanner: str
    severity: str
    category: str
    title: str
    description: str
    file_path: str
    line_number: Optional[int]
    rule_id: str
    remediation: Optional[str]
    confidence: str

class ScanResult(BaseModel):
    repo_url: str
    repo_name: str
    health_score: int
    grade: str
    findings: List[Finding]
    counts: dict
    ai_summary: str
    duration: float
