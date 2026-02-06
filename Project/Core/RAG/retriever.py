from __future__ import annotations
from typing import Dict, List
from Core.RAG.embeddings import embed_texts
from Core.RAG.chroma_store import query_chunks


DIMENSION_QUERIES = {
    "skills_match": "Required skills, tools, frameworks, technologies, must-have keywords.",
    "experience": "Relevant work experience, responsibilities, years, production deployment, ownership.",
    "projects_impact": "Projects demonstrating end-to-end work, measurable impact, systems built, complexity.",
    "engineering_maturity": "APIs, deployment, Docker, CI/CD, cloud, testing, monitoring, pipelines.",
    "communication_clarity": "Clear bullet points, quantified results, concise role alignment.",
}

# ✅ In-memory cache so we don't embed the same queries every click
_QUERY_EMB_CACHE: Dict[str, List[float]] = {}
#_QUERY_EMB_CACHE is an in‑memory dictionary meant to cache the embedding vector for 
#each dimension query (so you don’t re‑embed the same query every time).
def _snippet(text: str, max_words: int = 40) -> str:
    words = text.strip().split()
    return " ".join(words[:max_words])

def _get_query_embedding(dim: str, query: str) -> List[float]:
    if dim in _QUERY_EMB_CACHE:
        return _QUERY_EMB_CACHE[dim]
    vec = embed_texts([query])[0]
    _QUERY_EMB_CACHE[dim] = vec
    return vec

def retrieve_evidence(run_id: str, top_k: int = 5) -> Dict:
    """
    For each dimension:
      - query JD collection
      - query RESUME collection
    """
    out = {"run_id": run_id, "top_k": top_k, "dimensions": []}

    for dim, q in DIMENSION_QUERIES.items():
        q_emb = embed_texts([q])[0]

        jd_hits = query_chunks("jd_chunks", q_emb, run_id=run_id, top_k=top_k)
        res_hits = query_chunks("resume_chunks", q_emb, run_id=run_id, top_k=top_k)

        out["dimensions"].append({
            "dimension": dim,
            "query": q,
            "jd_evidence": [
                {
                    "chunk_id": h["chunk_id"],
                    "snippet": _snippet(h["text"]),
                    "section": h["metadata"].get("section"),
                    "start_char": h["metadata"].get("start_char"),
                    "end_char": h["metadata"].get("end_char"),
                    "distance": h["distance"],
                } for h in jd_hits
            ],
            "resume_evidence": [
                {
                    "chunk_id": h["chunk_id"],
                    "snippet": _snippet(h["text"]),
                    "section": h["metadata"].get("section"),
                    "start_char": h["metadata"].get("start_char"),
                    "end_char": h["metadata"].get("end_char"),
                    "distance": h["distance"],
                } for h in res_hits
            ]
        })

    return out
