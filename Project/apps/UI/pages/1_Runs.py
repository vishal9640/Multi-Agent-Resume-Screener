import os
import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

API_BASE = os.getenv("API_BASE_URL", "http://localhost:8000")

st.set_page_config(page_title="Run History", layout="wide")
st.title("Run History")

limit = st.slider("How many runs to show?", min_value=5, max_value=100, value=20, step=5)

try:
    r = requests.get(f"{API_BASE}/runs", params={"limit": limit}, timeout=30)
    if r.status_code != 200:
        st.error(f"Failed: {r.status_code} — {r.text}")
    else:
        runs = r.json().get("runs", [])
        if not runs:
            st.warning("No runs found yet. Go to Home and create one.")
        else:
            st.table(runs)
except Exception as e:
    st.error(str(e))