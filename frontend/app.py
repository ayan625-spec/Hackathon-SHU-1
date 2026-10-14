import streamlit as st
import httpx
import os
import pandas as pd
import plotly.graph_objects as go
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="DevFlow Sentinel", page_icon="🛡️", layout="wide")

# Custom CSS for Glassmorphism
st.markdown("""
<style>
    .stApp {
        background-color: #0D1117;
        color: #C9D1D9;
    }
    .glass-card {
        background: rgba(22, 27, 34, 0.7);
        border: 1px solid rgba(48, 54, 61, 1);
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 20px;
        backdrop-filter: blur(10px);
    }
    .metric-card {
        text-align: center;
        padding: 15px;
        border-radius: 10px;
        background: rgba(255, 255, 255, 0.03);
    }
    .severity-critical { color: #EF4444; font-weight: bold; }
    .severity-high { color: #F59E0B; font-weight: bold; }
    .severity-medium { color: #3B82F6; font-weight: bold; }
    .severity-low { color: #10B981; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

def render_health_gauge(score, grade):
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = score,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': f"Health Grade: {grade}", 'font': {'size': 24, 'color': "#00D4FF"}},
        gauge = {
            'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "white"},
            'bar': {'color': "#00D4FF"},
            'bgcolor': "rgba(0,0,0,0)",
            'borderwidth': 2,
            'bordercolor': "#30363d",
            'steps': [
                {'range': [0, 40], 'color': 'rgba(239, 68, 68, 0.3)'},
                {'range': [40, 75], 'color': 'rgba(245, 158, 11, 0.3)'},
                {'range': [75, 100], 'color': 'rgba(16, 185, 129, 0.3)'}
            ],
            'threshold': {
                'line': {'color': "white", 'width': 4},
                'thickness': 0.75,
                'value': score
            }
        }
    ))
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', font={'color': "white", 'family': "Space Mono"})
    st.plotly_chart(fig, use_container_width=True)

def main():
    st.title("🛡️ DevFlow Sentinel")
    st.markdown("AI-Powered DevSecOps Intelligence for Engineering Teams")
    
    with st.sidebar:
        st.header("Scan Repository")
        repo_url = st.text_input("GitHub Repo URL", placeholder="https://github.com/username/repo")
        user_id = st.text_input("User ID (Optional)", value="guest")
        scan_button = st.button("Run Intelligence Scan", type="primary")

    if scan_button:
        if not repo_url:
            st.error("Please enter a repository URL.")
        else:
            with st.spinner("🔍 Cloning repo and orchestrating scanners..."):
                try:
                    backend_url = os.getenv("BACKEND_URL", "http://localhost:8000")
                    response = httpx.post(
                        f"{backend_url}/api/scan",
                        json={"repo_url": repo_url, "user_id": user_id},
                        timeout=120.0
                    )
                    
                    if response.status_code == 200:
                        data = response.json()
                        st.success(f"Analysis Complete for {data['repo_name']}!")
                        
                        col1, col2 = st.columns([1, 2])
                        
                        with col1:
                            render_health_gauge(data['health_score'], data['grade'])
                            
                        with col2:
                            st.subheader("AI Executive Summary")
                            st.markdown(data['ai_summary'])
                        
                        # Metrics Strip
                        m1, m2, m3, m4, m5 = st.columns(5)
                        counts = data['counts']
                        m1.metric("Critical", counts['critical'], delta_color="inverse")
                        m2.metric("High", counts['high'], delta_color="inverse")
                        m3.metric("Medium", counts['medium'], delta_color="normal")
                        m4.metric("Low", counts['low'], delta_color="normal")
                        m5.metric("Secrets", counts['secrets'], delta_color="inverse")
                        
                        # Findings Table
                        st.subheader("Detailed Findings")
                        if data['findings']:
                            df = pd.DataFrame(data['findings'])
                            st.dataframe(
                                df[['severity', 'category', 'title', 'file_path', 'line_number']],
                                use_container_width=True,
                                hide_index=True
                            )
                        else:
                            st.info("No major findings detected. Your repo looks clean!")
                            
                    else:
                        st.error(f"Error: {response.json().get('detail', 'Unknown error')}")
                except Exception as e:
                    st.error(f"Connection failed: {str(e)}")

    else:
        # Welcome State
        st.info("Enter a GitHub URL on the sidebar to begin the analysis.")
        
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown("<div class='glass-card'><h3>Security Analysis</h3><p>Static analysis (SAST) via Semgrep and Bandit to find SQLi, XSS, and more.</p></div>", unsafe_allow_html=True)
        with c2:
            st.markdown("<div class='glass-card'><h3>Secret Detection</h3><p>Detect leaked API keys, tokens, and credentials with GitLeaks.</p></div>", unsafe_allow_html=True)
        with c3:
            st.markdown("<div class='glass-card'><h3>Tech Debt</h3><p>Analyze cyclomatic complexity and maintainability via Radon.</p></div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
