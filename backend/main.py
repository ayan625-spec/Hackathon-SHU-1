import os
import sys
import time
from datetime import datetime
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.models.scan_models import ScanRequest, ScanResult
from services.github_service import GitHubService
from services.scanner_orchestrator import ScannerOrchestrator
from services.health_score_engine import HealthScoreEngine
from services.ai_insight_service import AIInsightService
from parsers.semgrep_parser import SemgrepParser
from parsers.bandit_parser import BanditParser
from parsers.gitleaks_parser import GitLeaksParser
from parsers.radon_parser import RadonParser
from app_db.database import AppwriteDatabase

load_dotenv()

app = FastAPI(title="DevFlow Sentinel API", version="1.0.0")

# Restrict CORS to the Streamlit frontend only
_allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:8501").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in _allowed_origins],
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)

# Singletons — instantiated once at startup, not per request
_ai_service = AIInsightService()
_db = AppwriteDatabase()


@app.get("/health")
async def health():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}


@app.post("/api/scan", response_model=ScanResult)
async def scan_repository(request: ScanRequest):
    start_time = time.time()
    repo_path = None
    try:
        repo_path, repo_name = GitHubService.clone_repository(request.repo_url)

        orchestrator = ScannerOrchestrator(repo_path)
        raw_results = await orchestrator.run_all()

        all_findings = []
        all_findings.extend(SemgrepParser().parse(raw_results["semgrep"]))
        all_findings.extend(BanditParser().parse(raw_results["bandit"]))
        all_findings.extend(GitLeaksParser().parse(raw_results["gitleaks"]))
        all_findings.extend(RadonParser().parse(raw_results["radon"]))

        health_data = HealthScoreEngine.calculate_score(all_findings)

        ai_summary = await _ai_service.generate_executive_summary({
            "counts": health_data["counts"],
            "score": health_data["score"],
            "repo_name": repo_name,
        })

        scan_result = {
            "repo_url":     request.repo_url,
            "repo_name":    repo_name,
            "health_score": health_data["score"],
            "grade":        health_data["grade"],
            "findings":     all_findings,
            "counts":       health_data["counts"],
            "ai_summary":   ai_summary,
            "duration":     time.time() - start_time,
            "scanned_at":   datetime.now().isoformat(),
            "user_id":      request.user_id,
        }

        # Non-blocking persistence — DB failure must not break the scan response
        try:
            _db.save_scan(scan_result)
        except Exception as db_err:
            print(f"[DB] Save failed (non-fatal): {db_err}")

        return scan_result

    except HTTPException:
        raise
    except Exception as e:
        # Log full detail server-side; return a safe message to the client
        print(f"[SCAN ERROR] {type(e).__name__}: {e}")
        raise HTTPException(
            status_code=500,
            detail="Scan failed. Please check the repository URL and try again.",
        )
    finally:
        if repo_path:
            GitHubService.cleanup(repo_path)


@app.post("/api/remediate")
async def remediate_finding(payload: dict):
    """Endpoint for the per-finding AI Fix button in the frontend."""
    finding = payload.get("finding", {})
    remediation = await _ai_service.generate_remediation(finding)
    return {"remediation": remediation}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host=os.getenv("FASTAPI_HOST", "0.0.0.0"),
        port=int(os.getenv("FASTAPI_PORT", 8000)),
    )
