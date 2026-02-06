# Import required libraries for web UI and API communication
import os
import requests
import streamlit as st
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get API base URL from environment or use default
API_BASE = os.getenv("API_BASE_URL", "http://localhost:8000")

# Configure Streamlit page settings
st.set_page_config(page_title="Personal Resume Analyzer", layout="wide")
st.title("Personal Multi-Agent Resume Analyzer (Phase 1)")
st.caption("Upload/paste a JD and resume → create a run → view history. (Analysis is dummy in Phase 1.)")

# Sidebar for API configuration and health check
with st.sidebar:
    st.subheader("API")
    st.write(f"Base URL: `{API_BASE}`")
    # Button to verify API is running
    if st.button("Health Check"):
        try:
            r = requests.get(f"{API_BASE}/health", timeout=10)
            st.success(r.json())
        except Exception as e:
            st.error(str(e))

# Create two-column layout for inputs
col1, col2 = st.columns(2)

# Left column: Job Description input
with col1:
    st.subheader("Job Description (JD)")
    jd_file = st.file_uploader("Upload JD (PDF/DOCX/TXT)", type=["pdf", "docx", "txt"], key="jd_file")
    jd_text = st.text_area("Or paste JD text", height=220, key="jd_text")

# Right column: Resume input
with col2:
    st.subheader("Resume")
    resume_file = st.file_uploader("Upload Resume (PDF/DOCX/TXT)", type=["pdf", "docx", "txt"], key="resume_file")
    resume_text = st.text_area("Or paste resume text", height=220, key="resume_text")

st.divider()

# Create button and info section
colA, colB = st.columns([1, 2])

with colA:
    create_run = st.button("✅ Create Run", use_container_width=True)

with colB:
    st.info("Tip: In Phase 1, PDF/DOCX content is stored as a placeholder text. Parsing comes in Phase 2.")

# Handle run creation when button is clicked
if create_run:
    files = {}
    data = {}

    # Add pasted text to form data if provided
    if jd_text.strip():
        data["jd_text"] = jd_text
    if resume_text.strip():
        data["resume_text"] = resume_text

    # Add files only if no pasted text was provided (pasted text takes priority)
    if jd_file is not None and not jd_text.strip():
        files["jd_file"] = (jd_file.name, jd_file.getvalue(), jd_file.type)
    if resume_file is not None and not resume_text.strip():
        files["resume_file"] = (resume_file.name, resume_file.getvalue(), resume_file.type)

    try:
        # Send POST request to ingest endpoint with form data and/or files
        r = requests.post(f"{API_BASE}/ingest", data=data, files=files if files else None, timeout=60)
        if r.status_code != 200:
            st.error(f"Failed: {r.status_code} — {r.text}")
        else:
            # Display success message and response data
            payload = r.json()
            st.success(f"Run created! run_id = {payload['run_id']}")
            st.json(payload)

            # Optional button to trigger Phase 1 dummy analysis
            if st.button("Run Dummy Analyze Now"):
                a = requests.post(f"{API_BASE}/analyze/{payload['run_id']}", timeout=60)
                st.write(a.status_code)
                st.json(a.json())
    except Exception as e:
        st.error(str(e))
