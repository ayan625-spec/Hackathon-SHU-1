import asyncio
import subprocess
import json
import os
import tempfile
import uuid
from typing import List, Dict, Any

class GitLeaksScanner:
    async def scan(self, repo_path: str) -> List[Dict[str, Any]]:
        report_path = os.path.join(tempfile.gettempdir(), f"gitleaks_{uuid.uuid4().hex}.json")
        try:
            cmd = ["gitleaks", "detect", "--source", repo_path, "--report-format", "json", "--report-path", report_path]
            process = await asyncio.create_subprocess_exec(*cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            await process.communicate()
            
            if os.path.exists(report_path):
                with open(report_path, "r") as f:
                    data = json.load(f)
                os.remove(report_path)
                return data
            return []
        except Exception as e:
            print(f"GitLeaks Error: {e}")
            return []
