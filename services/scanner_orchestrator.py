import asyncio
from typing import Dict, Any
from scanners.semgrep_scanner import SemgrepScanner
from scanners.bandit_scanner import BanditScanner
from scanners.gitleaks_scanner import GitLeaksScanner
from scanners.radon_scanner import RadonScanner

class ScannerOrchestrator:
    def __init__(self, repo_path: str):
        self.repo_path = repo_path
        self.semgrep = SemgrepScanner()
        self.bandit = BanditScanner()
        self.gitleaks = GitLeaksScanner()
        self.radon = RadonScanner()

    async def run_all(self) -> Dict[str, Any]:
        results = await asyncio.gather(
            self.semgrep.scan(self.repo_path),
            self.bandit.scan(self.repo_path),
            self.gitleaks.scan(self.repo_path),
            self.radon.scan(self.repo_path)
        )
        
        return {
            "semgrep": results[0],
            "bandit": results[1],
            "gitleaks": results[2],
            "radon": results[3]
        }
