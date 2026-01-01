# Personal Multi-Agent Resume Analyzer (LLM + RAG)

A **production-quality, local-only AI system** that analyzes how well a resume matches a job description using **LLMs, RAG, and multi-agent orchestration**.  
Built for **personal job search use**, but designed with **real-world engineering standards** — explainability, evaluation, logging, and reproducibility.

This is **not a toy project**. It is intended to demonstrate **system design, agentic AI, and responsible LLM usage** at an interview-ready level.

Why this is a multi-agent system
This project uses a multi-agent design where multiple role-specialized LLM agents perform distinct tasks within a single orchestrated workflow. Each agent has a clearly defined responsibility—resume extraction, rubric-based scoring with citations, gap analysis with improvement recommendations, and interview question generation—and operates on a shared structured state managed by a LangGraph state machine. This separation of concerns improves explainability, evaluation, and stability compared to a single monolithic prompt, making the system production-oriented rather than a toy LLM demo.
---

## 🚀 What This Project Does

Given:
- A **Job Description (JD)**  
- A **Resume**  

The system:
1. Scores the resume against the JD using a **structured rubric**
2. Explains **why** each score was given using **evidence-backed citations**
3. Identifies **missing skills, keywords, and seniority gaps**
4. Suggests **permission-based resume improvements** (bullet rewrites + ATS optimization)
5. Generates **role-specific interview questions** (basic → advanced)
6. Tracks **resume improvements across multiple iterations (v1 → v2 → v3)**

All processing runs **locally**.

---

## 🧠 Key Design Principles

- **Explainability-first**  
  Every score must include citations from both the JD and resume.
- **Deterministic & auditable**  
  Inputs, outputs, prompts, models, and token usage are logged.
- **Permission-based editing**  
  Resume changes are suggested — never applied without approval.
- **Production mindset**  
  Schema validation, stability checks, logging, and evaluation are mandatory.

---

## 🏗️ High-Level Architecture

```
Streamlit UI
    ↓
FastAPI Backend
    ↓
LangGraph Orchestrator (Multi-Agent)
    ↓
 ┌───────────────┬───────────────┐
 │  Ollama LLM   │  Chroma Vector │
 │ (local)       │  DB (RAG)      │
 └───────────────┴───────────────┘
    ↓
Postgres (Runs, Logs, Versions)
```

---

## 🔄 End-to-End Pipeline

### 1. Ingest
- Upload or paste:
  - Job Description (PDF / DOCX / TXT)
  - Resume (PDF / DOCX / TXT)
- Inputs are hashed for reproducibility.

### 2. Parse & Normalize
- Convert raw text into structured JSON:
  - skills, experience, projects, education, bullets
- **Provenance preserved**:
  every extracted field maps back to source text spans.

### 3. RAG (Retrieval-Augmented Generation)
- JD is chunked and embedded into **Chroma**
- Optional rubric guidelines are also embedded
- All scoring is grounded in retrieved context only

### 4. Multi-Agent Evaluation (LangGraph)
Agents run in a controlled state machine:
- **Extractor Agent** → structured candidate profile
- **Matcher / Scorer Agent** → rubric-based scoring + citations
- **Gap Agent** → missing skills & improvement actions
- **Interview Question Agent** → role-specific questions

### 5. Outputs
- Overall score (0–100) + dimension breakdown
- Evidence-backed citations
- Skill gaps + resume improvement suggestions
- Interview questions with evaluation signals

### 6. Storage & Logging
Each run persists:
- input hashes
- outputs
- agent decisions
- prompts & model versions
- token usage & timings

---

## 📊 Scoring Rubric (Adaptive)

Base rubric (0–100):
- Skills match — 30
- Relevant experience — 25
- Projects & impact — 20
- Engineering maturity — 15
- Communication clarity — 10

**Hard rejection flags** are raised for:
- Missing must-have JD skills
- Explicit JD constraints not met

---

## 📌 Citation Contract (Non-Negotiable)

Every scored dimension **must include**:
- JD citation(s)
- Resume citation(s) **or** explicit `missing_evidence = true`

Citation format:
```json
{
  "chunk_id": "JD-0012",
  "quote": "deploy ML models to production",
  "relevance": "Must-have requirement",
  "span": { "start_char": 1200, "end_char": 1240 }
}
```

If citations are missing → recommendation is blocked.

---

## ✍️ Resume Improvement Loop

- Suggest bullet rewrites and ATS keyword improvements
- Show **diff preview**
- User approves selected changes
- New resume version generated:
  - v1 → v2 → v3
- Export format:
  - DOCX or PDF (user-selected)

---

## 🎤 Interview Preparation

- Questions generated from **JD + Resume**
- Difficulty levels:
  - Basic
  - Intermediate
  - Advanced
- Each question includes:
  - Skill tag
  - Why it’s asked
  - Strong answer signals
  - Likely interview risk (if applicable)

---

## 🧪 Evaluation & Stability

Automated checks:
- Schema validation (100% required)
- Citation coverage (100% required)
- Quote length enforcement
- Score stability across reruns

Personal effectiveness metrics:
- Resume score improvement
- Keyword coverage delta
- Hard-flag resolution rate
- Interview risk reduction

---

## 🛠️ Tech Stack

- **LLM:** Ollama (local, balanced tier)
- **Embeddings:** nomic-embed-text
- **Agent Orchestration:** LangGraph
- **Vector DB:** Chroma
- **Backend:** FastAPI
- **UI:** Streamlit
- **Database:** Postgres (local)
- **Storage:** Local filesystem

---

## ⏱️ Development Timeline

| Phase | Duration |
|-----|----------|
| Project setup & UI skeleton | 1–2 days |
| Parsing & provenance | 2 days |
| RAG & chunking | 2 days |
| Multi-agent orchestration | 3 days |
| Resume improvement loop | 2 days |
| Evaluation & logging | 2 days |
| Polish & documentation | 1 day |

**Total:** ~12–14 days

---

## 🎯 Why This Project Matters

This project demonstrates:
- Multi-agent LLM system design
- Explainable AI with evidence enforcement
- RAG grounded decision-making
- Evaluation discipline
- Ethical resume optimization
- Production-style engineering thinking

---

## 📌 Future Enhancements
- Prompt versioning & regression testing
- Resume/JD comparison analytics
- Optional cloud toggle
- Recruiter-mode (multi-tenant) extension

---

## 🧑‍💻 Author
Built as a **personal AI job-search copilot** and **portfolio project**  
by an AI/ML Engineer focused on **GenAI, agentic systems, and production AI**.
