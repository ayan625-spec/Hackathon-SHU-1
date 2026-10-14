import os
from google import genai
from typing import Dict, Any
from dotenv import load_dotenv

load_dotenv()

_DEFAULT_MODEL = "gemini-2.0-flash"


def _ai_error_message(error: Exception, feature: str) -> str:
    """Return safe user-facing text without exposing provider request details."""
    detail = str(error).lower()
    if "consumer_suspended" in detail or "has been suspended" in detail:
        return (
            f"{feature} unavailable: the Google AI key or project is suspended. "
            "Replace GEMINI_API_KEY with an active key and verify the project's access."
        )
    if "permission_denied" in detail or "403" in detail:
        return (
            f"{feature} unavailable: Google AI access was denied. "
            "Check GEMINI_API_KEY and the associated project's API access."
        )
    return f"{feature} unavailable: the Google AI request failed. Check the AI configuration."


class AIInsightService:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        self.model = os.getenv("GEMINI_MODEL", _DEFAULT_MODEL)
        if api_key:
            self.client = genai.Client(api_key=api_key)
        else:
            self.client = None

    async def generate_executive_summary(self, data: Dict[str, Any]) -> str:
        if not self.client:
            return "AI Insights unavailable (No API Key)."
            
        prompt = f"""
        You are a senior DevSecOps engineer reviewing scan results.
        Given: Finding Counts: {data.get('counts')}, Health Score: {data.get('score')}, Repo: {data.get('repo_name')}
        Generate a 3-paragraph executive summary covering:
        1. Overall security posture
        2. Most critical risks requiring immediate attention
        3. Business impact and recommended next steps
        Keep it concise, professional, and investor-demo ready.
        """
        
        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt
            )
            return response.text if response.text else "AI failed to generate summary."
        except Exception as e:
            return _ai_error_message(e, "AI insights")

    async def generate_remediation(self, finding: Dict[str, Any]) -> str:
        if not self.client:
            return "Remediation guidance unavailable."
            
        prompt = f"""
        You are a security engineer. For this finding:
        Title: {finding.get('title')}, Description: {finding.get('description')}, File: {finding.get('file_path')}
        Provide:
        1. Root cause (1 sentence)
        2. Fix (code snippet or specific steps)
        3. Prevention (1 sentence)
        Be direct and actionable.
        """
        
        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt
            )
            return response.text if response.text else "AI failed to generate remediation."
        except Exception as e:
            return _ai_error_message(e, "AI remediation")
