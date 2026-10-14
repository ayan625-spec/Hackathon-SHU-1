from pydantic import BaseModel, field_validator
from typing import Optional, List
import re


class ScanRequest(BaseModel):
    repo_url: str
    user_id: str = "guest"

    @field_validator("repo_url")
    @classmethod
    def validate_github_url(cls, v: str) -> str:
        """Only allow public GitHub HTTPS URLs to prevent SSRF."""
        pattern = r"^https://github\.com/[\w.\-]+/[\w.\-]+(\.git)?/?$"
        if not re.match(pattern, v):
            raise ValueError(
                "repo_url must be a valid GitHub HTTPS URL "
                "(e.g. https://github.com/owner/repo)"
            )
        return v.rstrip("/")


class Finding(BaseModel):
    scanner: str
    severity: str
    category: str
    title: str
    description: str
    file_path: Optional[str] = None
    line_number: Optional[int] = None
    rule_id: Optional[str] = None
    remediation: Optional[str] = None
    confidence: str = "medium"


class ScanResult(BaseModel):
    repo_url: str
    repo_name: str
    health_score: int
    grade: str
    findings: List[Finding]
    counts: dict
    ai_summary: str
    duration: float
    scanned_at: str
    user_id: str = "guest"
