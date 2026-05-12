import os
import sys
import time
import asyncio
from datetime import datetime
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Add project root to sys.path
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

app = FastAPI(title="DevFlow Sentinel API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.post("/api/scan", response_model=ScanResult)
async def scan_repository(request: ScanRequest):
    start_time = time.time()
    repo_path = None
    
    try:
        # 1. Clone Repo
        github = GitHubService()
        repo_path, repo_name = github.clone_repository(request.repo_url)
        
        # 2. Orchestrate Scanners
        orchestrator = ScannerOrchestrator(repo_path)
        raw_results = await orchestrator.run_all()
        
        # 3. Parse Results
        all_findings = []
        all_findings.extend(SemgrepParser().parse(raw_results["semgrep"]))
        all_findings.extend(BanditParser().parse(raw_results["bandit"]))
        all_findings.extend(GitLeaksParser().parse(raw_results["gitleaks"]))
        all_findings.extend(RadonParser().parse(raw_results["radon"]))
        
        # 4. Calculate Health Score
        health_data = HealthScoreEngine.calculate_score(all_findings)
        
        # 5. AI Insights
        ai_service = AIInsightService()
        summary_data = {
            "counts": health_data["counts"],
            "score": health_data["score"],
            "repo_name": repo_name
        }
        ai_summary = await ai_service.generate_executive_summary(summary_data)
        
        duration = time.time() - start_time
        
        # Assemble Result
        scan_result = {
            "repo_url": request.repo_url,
            "repo_name": repo_name,
            "health_score": health_data["score"],
            "grade": health_data["grade"],
            "findings": all_findings,
            "counts": health_data["counts"],
            "ai_summary": ai_summary,
            "duration": duration,
            "scanned_at": datetime.now().isoformat(),
            "user_id": request.user_id
        }
        
        # 6. Save to Appwrite
        db = AppwriteDatabase()
        db.save_scan(scan_result)
        
        return scan_result
        
    except Exception as e:
        print(f"Scan Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if repo_path:
            GitHubService.cleanup(repo_path)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
