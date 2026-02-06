import os
import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()
API_BASE = os.getenv("API_BASE_URL", "http://localhost:8000")


st.set_page_config(page_title="RAG Playground", layout="wide")
st.title("Phase 3 — RAG Playground (Chroma + Ollama Embeddings)")

run_id = st.text_input("Enter run_id").strip()

top_k = st.slider("Top-K evidence per dimension", min_value=1, max_value=10, value=5, step=1)

col1, col2 = st.columns(2)

rid = run_id.strip()

with col1:
    if st.button("📌 Index JD + Resume into Chroma", use_container_width=True):
        if not run_id:
            st.error("Please enter run_id")
        else:
            r = requests.post(f"{API_BASE}/rag/index/{rid}", timeout=180) # API call to rag_routes.py #Here we are making a POST request to the API endpoint to index the JD and resume for the given run_id into the Chroma DB.
            if r.status_code != 200:
                st.error(f"Failed: {r.status_code} — {r.text}")
            else:
                st.success("Indexing complete ✅")
                st.json(r.json())

with col2:
    if st.button("🔎 Test Retrieval", use_container_width=True):
        if not run_id.strip():
            st.error("Please enter run_id")
        else:
            r = requests.post(f"{API_BASE}/rag/retrieve/{rid}", params={"top_k": top_k}, timeout=180) #Here we are making a POST request to the API endpoint to retrieve evidence for the given run_id and top_k value.
            if r.status_code != 200:
                st.error(f"Failed: {r.status_code} — {r.text}")
            else:
                payload = r.json()
                st.success("Retrieval complete ✅")

                for dim in payload.get("dimensions", []):
                    st.subheader(f"Dimension: {dim['dimension']}")
                    st.caption(dim.get("query", ""))

                    c1, c2 = st.columns(2)
                    with c1:
                        st.markdown("### JD Evidence")
                        for e in dim.get("jd_evidence", []):
                            dist = e.get("distance", None)
                            dist_str = f"{dist:.4f}" if isinstance(dist, (int, float)) else "NA"

                            st.write(
                                f"**{e.get('chunk_id','?')}** | section: `{e.get('section','?')}` | dist: `{dist_str}`"
                            )
                            st.write(e.get("snippet", "") or "")
                            st.divider()

                    with c2:
                        st.markdown("### Resume Evidence")
                        for e in dim.get("resume_evidence", []):
                            dist = e.get("distance", None)
                            dist_str = f"{dist:.4f}" if isinstance(dist, (int, float)) else "NA"

                            st.write(
                                f"**{e.get('chunk_id','?')}** | section: `{e.get('section','?')}` | dist: `{dist_str}`"
                            )
                            st.write(e.get("snippet", "") or "")
                            st.divider()            
