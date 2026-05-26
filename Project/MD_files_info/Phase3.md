# Phase 3 – System Architecture & Agent Design

## Objective
Define **how the system is built**, using production-grade patterns.

---

## Architecture Overview

### Backend
- FastAPI
- Handles ingestion, orchestration, persistence

### Agent Orchestration
- LangChain / LangGraph
- State-machine-based execution

### Vector Storage
- JD embeddings → Vector Store
- Rubric embeddings → Vector Store

### Database
- SQLite (local) or Postgres (cloud)
- Stores runs, logs, outputs

### UI
- Streamlit dashboard

---

## Pipeline Breakdown

### 1. Ingestion
- File upload → text extraction
- Chunking with metadata:
  - chunk_id
  - source (JD / RESUME / RUBRIC)
  - section
  - text span

### 2. RAG Layer
- Embedding generation
- Vector similarity search
- Citation-aware retrieval

---

## Agent Graph (LangGraph)

### Shared State Object
```json
{
  "parsed_resume": {},
  "jd_chunks": [],
  "rubric_chunks": [],
  "scores": {},
  "citations": [],
  "gaps": [],
  "interview_questions": []
}
