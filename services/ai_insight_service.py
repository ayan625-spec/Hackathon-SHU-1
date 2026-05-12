import os
from google import genai
from typing import List, Dict, Any
from dotenv import load_dotenv

load_dotenv()

class AIInsightService:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        self.model = os.getenv("GEMINI_MODEL", "gemini-1.5")
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
            return f"AI Error: {str(e)}"

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
            return f"AI Error: {str(e)}"
