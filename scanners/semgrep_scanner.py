import asyncio
import subprocess
import json
from typing import Dict, Any

class SemgrepScanner:
    async def scan(self, repo_path: str) -> Dict[str, Any]:
        try:
            cmd = ["semgrep", "--config=p/security-audit", "--config=p/python", "--json", "--quiet", "--timeout=60", repo_path]
            process = await asyncio.create_subprocess_exec(*cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, _ = await process.communicate()
            if stdout:
                return json.loads(stdout.decode())
            return {"results": []}
        except Exception as e:
            print(f"Semgrep Error: {e}")
            return {"results": []}
