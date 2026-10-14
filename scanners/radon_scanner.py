import asyncio
import json
from typing import Dict, Any

_TIMEOUT = 60  # seconds


class RadonScanner:
    async def scan(self, repo_path: str) -> Dict[str, Any]:
        try:
            proc_cc = await asyncio.create_subprocess_exec(
                "radon", "cc", repo_path, "-j",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            out_cc, _ = await asyncio.wait_for(proc_cc.communicate(), timeout=_TIMEOUT)
            cc_data = json.loads(out_cc.decode()) if out_cc else {}

            proc_mi = await asyncio.create_subprocess_exec(
                "radon", "mi", repo_path, "-j",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            out_mi, _ = await asyncio.wait_for(proc_mi.communicate(), timeout=_TIMEOUT)
            mi_data = json.loads(out_mi.decode()) if out_mi else {}

            return {"cc": cc_data, "mi": mi_data}

        except asyncio.TimeoutError:
            print(f"[Radon] Timed out after {_TIMEOUT}s")
            return {"cc": {}, "mi": {}}
        except Exception as e:
            print(f"[Radon] Error: {e}")
            return {"cc": {}, "mi": {}}
