from fastapi import APIRouter, HTTPException
from typing import Dict
import traceback

# ---- Parsing / Sectionizers ----
from Core.parsing.sectionizer import split_resume_sections
from Core.parsing.jd_sectionizer import split_jd_sections

# ---- RAG / Chroma ----
from Core.RAG.chroma_store import upsert_chunks
from Core.RAG.embeddings import embed_texts
from Core.RAG.chunking import sha256_text

# ---- DB access (runs table) ----
from apps.api.db import get_run_texts

router = APIRouter(prefix="/rag", tags=["rag"])


# =========================================================
# INDEX ENDPOINT
# =========================================================
@router.post("/index/{run_id}")
def index_run(run_id: str):
    """
    Index JD + Resume using SECTIONIZER-BASED CHUNKS.
    - JD chunks = JD sections
    - Resume chunks = Resume sections
    """

    try:
        # -------------------------------------------------
        # 1) Load raw JD + Resume text for this run
        # -------------------------------------------------
        jd_text, resume_text = get_run_texts(run_id)

        if not jd_text or not resume_text:
            raise HTTPException(status_code=400, detail="JD or Resume text missing for run")

        # -------------------------------------------------
        # 2) JD section-based chunks
        # -------------------------------------------------
        jd_sections = split_jd_sections(jd_text)
        jd_chunks = []
        j = 1

        for sec_name, sec in jd_sections.items():
            sec_text = (sec.get("text") or "").strip()
            if not sec_text:
                continue

            jd_chunks.append({
                "chunk_id": f"JD-{sec_name.upper()}-{j:04d}",
                "run_id": run_id,
                "source": "JD",
                "section": sec_name,
                "start_char": int(sec.get("start_char", 0)),
                "end_char": int(sec.get("end_char", 0)),
                "text": sec_text,
                "hash": sha256_text(sec_text),
            })
            j += 1

        # -------------------------------------------------
        # 3) Resume section-based chunks
        # -------------------------------------------------
        res_sections = split_resume_sections(resume_text)
        resume_chunks = []
        r = 1

        for sec_name, sec in res_sections.items():
            sec_text = (sec.get("text") or "").strip()
            if not sec_text:
                continue

            resume_chunks.append({
                "chunk_id": f"RES-{sec_name.upper()}-{r:04d}",
                "run_id": run_id,
                "source": "RESUME",
                "section": sec_name,
                "start_char": int(sec.get("start_char", 0)),
                "end_char": int(sec.get("end_char", 0)),
                "text": sec_text,
                "hash": sha256_text(sec_text),
            })
            r += 1

        # -------------------------------------------------
        # 4) Safety check
        # -------------------------------------------------
        if not jd_chunks:
            raise HTTPException(status_code=500, detail="No JD chunks produced")

        if not resume_chunks:
            raise HTTPException(status_code=500, detail="No Resume chunks produced")

        print("✅ JD chunks:", len(jd_chunks))
        print("✅ Resume chunks:", len(resume_chunks))
        print("✅ Resume sections:", [c["section"] for c in resume_chunks])

        # -------------------------------------------------
        # 5) Embeddings
        # -------------------------------------------------
        jd_embs = embed_texts([c["text"] for c in jd_chunks])
        res_embs = embed_texts([c["text"] for c in resume_chunks])

        # -------------------------------------------------
        # 6) Upsert into Chroma
        # -------------------------------------------------
        upsert_chunks("jd_chunks", jd_chunks, jd_embs)
        upsert_chunks("resume_chunks", resume_chunks, res_embs)

        return {
            "run_id": run_id,
            "jd_chunks_indexed": len(jd_chunks),
            "resume_chunks_indexed": len(resume_chunks),
            "jd_sections": list(jd_sections.keys()),
            "resume_sections": list(res_sections.keys()),
        }

    except HTTPException:
        raise
    except Exception:
        print("❌ Error during /rag/index")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail="Indexing failed")


# =========================================================
# RETRIEVE ENDPOINT
# =========================================================
from Core.RAG.retriever import retrieve_evidence

@router.post("/retrieve/{run_id}")
def retrieve_run(run_id: str, top_k: int = 5):
    """
    Retrieve evidence per scoring dimension.
    """
    try:
        return retrieve_evidence(run_id=run_id, top_k=top_k)
    except Exception:
        print("❌ Error during /rag/retrieve")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail="Retrieval failed")


# =========================================================
# OPTIONAL GET ENDPOINTS (for browser testing)
# =========================================================
@router.get("/index/{run_id}")
def index_run_get(run_id: str):
    return index_run(run_id)

@router.get("/retrieve/{run_id}")
def retrieve_run_get(run_id: str, top_k: int = 5):
    return retrieve_run(run_id, top_k)
