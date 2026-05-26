import os
import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()
API_BASE = os.getenv("API_BASE_URL", "http://localhost:8000")

st.set_page_config(page_title="Parse (Phase 2)", layout="wide")
st.title("Phase 2 — Parse JD & Resume")

run_id = st.text_input("Enter run_id (from Home or Runs page)")

if st.button("Run Parse"):
    if not run_id.strip():
        st.error("Please enter a run_id")
    else:
        try:
            r = requests.post(f"{API_BASE}/parse/{run_id}", timeout=90)
            if r.status_code != 200:
                st.error(f"Failed: {r.status_code} — {r.text}")
            else:
                payload = r.json()
                st.success("Parse complete ✅")

                col1, col2 = st.columns(2)
                with col1:
                    st.subheader("Parsed JD JSON")
                    st.json(payload.get("parsed_jd", {}))
                with col2:
                    st.subheader("Candidate Profile JSON")
                    st.json(payload.get("candidate_profile", {}))

                st.subheader("Resume Sections (with offsets)")
                st.json(payload.get("resume_sections", {}))
        except Exception as e:
            st.error(str(e))
