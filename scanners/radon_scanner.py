import asyncio
import subprocess
import json
from typing import Dict, Any

class RadonScanner:
    async def scan(self, repo_path: str) -> Dict[str, Any]:
        try:
            # Cyclomatic complexity
            cmd_cc = ["radon", "cc", repo_path, "-j"]
            process_cc = await asyncio.create_subprocess_exec(*cmd_cc, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout_cc, _ = await process_cc.communicate()
            
            cc_data = json.loads(stdout_cc.decode()) if stdout_cc else {}
            
            return {"cc": cc_data}
        except Exception as e:
            print(f"Radon Error: {e}")
            return {"cc": {}}
