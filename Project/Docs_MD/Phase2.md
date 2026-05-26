# PHASE 2 — RAG Layer + Vector Store (JD + Rubric) + Retrieval Contracts
**Project:** Personal Multi-Agent Resume Analyzer (LLM + RAG)  
**Phase:** 2 (Embeddings, vector store, retrieval, citation readiness)  
**Status:** Completed (as per architecture plan)

---

## 2.1 Objective
Implement RAG foundations:
- Embed + store JD chunks in vector DB
- Optionally embed + store rubric/guidelines as second vector store
- Provide retriever APIs for agents
- Ensure retrieval results carry chunk metadata for citation output

---

## 2.2 Data Stores
### Vector Stores
- `jd_store`: embeddings for JD chunks
- `rubric_store` (optional but strong): embeddings for rubric + scoring guidelines

### Persistence choice
- Local first: Chroma or FAISS
- Later: Pinecone (if deploying)

---

## 2.3 Embedding Strategy
- Embedding model chosen and stored in run metadata
- Store:
  - `chunk_id`
  - `source` (JD/RESUME/RUBRIC)
  - `text_content`
  - `start_char/end_char`
  - `sha256_hash`
  - `run_id`

---

## 2.4 Retrieval Contracts
### Retriever Inputs
- query text (e.g., rubric dimension prompt, skill query)
- top_k (default 5–10)
- filters: `source == JD` or `source == RUBRIC`

### Retriever Outputs
- ranked list of chunks:
  - `{chunk_id, text_content, score, metadata}`

These are used directly by agents to:
- cite evidence
- justify scoring decisions

---

## 2.5 Acceptance Criteria (Phase 2)
- [ ] JD chunks embedded + stored, retrievable by semantic query
- [ ] Rubric chunks embedded + stored (optional path works)
- [ ] Retrieval output preserves chunk_id + text + provenance metadata
- [ ] RAG layer integrates cleanly with LangChain/LangGraph agents

---

## 2.6 Python Files Implemented in This Phase
### Embeddings + Vector Store
- `apps/rag/embeddings.py`
- `apps/rag/vectorstore_jd.py`
- `apps/rag/vectorstore_rubric.py`
- `apps/rag/retriever.py`

### Rubric Content Loader
- `apps/rubric/rubric_loader.py`
- `apps/rubric/rubric_schema.py`

### API Routes (optional)
- `apps/api/routes/rag.py` (debug endpoint: query vector store)
