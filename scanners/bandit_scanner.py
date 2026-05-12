import asyncio
import subprocess
import json
from typing import Dict, Any

class BanditScanner:
    async def scan(self, repo_path: str) -> Dict[str, Any]:
        try:
            cmd = ["bandit", "-r", repo_path, "-f", "json", "-q"]
            process = await asyncio.create_subprocess_exec(*cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, _ = await process.communicate()
            if stdout:
                return json.loads(stdout.decode())
            return {"results": []}
        except Exception as e:
            print(f"Bandit Error: {e}")
            return {"results": []}
