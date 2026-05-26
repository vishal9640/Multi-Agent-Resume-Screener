import os
import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()
API_BASE = os.getenv("API_BASE_URL", "http://localhost:8000")

st.set_page_config(page_title="Score (Phase 4)", layout="wide")
st.title("Phase 4 — Scoring + Citations + Gaps + Interview Questions")

run_id = st.text_input("Enter run_id").strip()

colA, colB = st.columns([1, 1])

with colA:
    top_k = st.slider("Top-K evidence per dimension (Phase 3 retriever)", 1, 10, 5, 1)
with colB:
    model_name = st.text_input("Ollama model (Phase 4)", value=os.getenv("OLLAMA_CHAT_MODEL", "qwen3:8b")).strip()

st.caption(f"API_BASE = {API_BASE}")

def pill(label, value):
    st.metric(label, value)

def show_citations(title, cits):
    st.markdown(f"**{title}**")
    if not cits:
        st.write("_No citations returned._")
        return
    for c in cits:
        st.write(f"- `{c.get('chunk_id','?')}` — “{c.get('quote','')}”")
        st.caption(c.get("relevance",""))

def group_questions(qs):
    buckets = {"basic": [], "intermediate": [], "advanced": []}
    for q in qs:
        lvl = q.get("level", "basic")
        buckets.setdefault(lvl, []).append(q)
    return buckets

if st.button("✅ Run Scoring", use_container_width=True):
    if not run_id:
        st.error("Please enter run_id")
    else:
        # If you want top_k configurable in Phase 4 graph, you can later pass it via state.
        # For now, score endpoint uses whatever retriever has configured.
        try:
            url = f"{API_BASE}/score/{run_id}"
            st.write("Calling:", url)
            r = requests.post(url, params={"mode": "fast"}, timeout=900)
            
            if st.button("Run Full (Gaps + Rewrites + Interview Qs)"):
                r = requests.post(url, params={"mode": "full"}, timeout=900)

            if not r.ok:
                st.error(f"Failed: {r.status_code}")
                st.code(r.text)
            else:
                out = r.json()

                st.success("Scoring complete ✅")

                # Summary row
                c1, c2, c3 = st.columns(3)
                with c1:
                    pill("Overall Score", out.get("overall_score", "NA"))
                with c2:
                    pill("Decision", out.get("decision", "NA"))
                with c3:
                    pill("Hard Reject", str(out.get("hard_reject", False)))

                if out.get("hard_flags"):
                    st.warning("Hard Flags")
                    st.json(out["hard_flags"])

                # Dimension scores
                st.subheader("Dimension Scores + Evidence")
                for d in out.get("dimension_scores", []):
                    with st.expander(f"{d['dimension']} — {d['score']} (weight {d['weight']})", expanded=False):
                        st.write(d.get("rationale", ""))

                        cc1, cc2 = st.columns(2)
                        with cc1:
                            show_citations("JD citations", d.get("jd_citations", []))
                        with cc2:
                            show_citations("Resume citations", d.get("resume_citations", []))

                # Gaps
                st.subheader("Skill / Keyword / Seniority Gaps")
                gaps = out.get("gaps", [])
                if not gaps:
                    st.write("_No gaps returned._")
                else:
                    st.json(gaps)

                # Rewrite suggestions (permission based)
                st.subheader("Resume Rewrite Suggestions (Permission-based)")
                rewrites = out.get("rewrites", [])
                if not rewrites:
                    st.write("_No rewrite suggestions returned._")
                else:
                    for i, rw in enumerate(rewrites[:20], start=1):
                        st.markdown(f"**{i}. Reason:** {rw.get('reason','')}")
                        st.write("Original:")
                        st.code(rw.get("original",""))
                        st.write("Suggested:")
                        st.code(rw.get("suggested",""))
                        st.caption("Requires permission: " + str(rw.get("requires_permission", True)))
                        st.divider()

                # Interview questions
                st.subheader("Interview Questions (Basic → Advanced)")
                qs = out.get("interview_questions", [])
                buckets = group_questions(qs)

                q1, q2, q3 = st.columns(3)
                with q1:
                    st.markdown("### Basic")
                    for q in buckets.get("basic", [])[:10]:
                        st.write(f"- **{q.get('skill_area','')}**: {q.get('question','')}")
                with q2:
                    st.markdown("### Intermediate")
                    for q in buckets.get("intermediate", [])[:10]:
                        st.write(f"- **{q.get('skill_area','')}**: {q.get('question','')}")
                with q3:
                    st.markdown("### Advanced")
                    for q in buckets.get("advanced", [])[:10]:
                        st.write(f"- **{q.get('skill_area','')}**: {q.get('question','')}")

                st.subheader("Full Score Output JSON")
                st.json(out)

        except Exception as e:
            st.exception(e)
