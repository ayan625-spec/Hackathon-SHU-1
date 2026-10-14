# DevFlow Sentinel

AI-native DevSecOps intelligence for engineering teams.

## Setup Instructions

### 1. Initialize Environment with uv
```bash
# uv is required
uv init
uv add streamlit fastapi uvicorn google-genai appwrite bandit radon semgrep pandas plotly pydantic httpx python-dotenv GitPython aiohttp
```

### 2. Configure Environment
Copy `.env.example` to `.env` and fill in your keys.

### 3. Run Backend
```bash
uv run python backend/main.py
```

### 4. Run Frontend
```bash
uv run streamlit run frontend/app.py
```

## Features
- GitHub Repository Scanner
- Security Scanner System (Semgrep, Bandit)
- Technical Debt Analyzer (Radon)
- Secret Detection (GitLeaks)
- AI Insight Generator (Gemini)
- Interactive Dashboard (Streamlit)
- Areeb as collaborator
