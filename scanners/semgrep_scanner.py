import asyncio
import json
from typing import Dict, Any

_TIMEOUT = 120  # seconds


class SemgrepScanner:
    async def scan(self, repo_path: str) -> Dict[str, Any]:
        cmd = [
            "semgrep",
            "--config=p/security-audit",
            "--json",
            "--quiet",
            "--timeout=60",
            repo_path,
        ]
        try:
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            stdout, _ = await asyncio.wait_for(process.communicate(), timeout=_TIMEOUT)
            return json.loads(stdout.decode()) if stdout else {"results": []}
        except asyncio.TimeoutError:
            print(f"[Semgrep] Timed out after {_TIMEOUT}s")
            return {"results": []}
        except Exception as e:
            print(f"[Semgrep] Error: {e}")
            return {"results": []}
