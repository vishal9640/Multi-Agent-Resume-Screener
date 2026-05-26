# PHASE 0 — Project Foundation & Requirements (MNC-style)
**Project:** Personal Multi-Agent Resume Analyzer (LLM + RAG)  
**Phase:** 0 (Discovery + Scope + Acceptance Criteria)  
**Owner:** You (Job Seeker / Builder)  
**Status:** Completed (as per current architecture freeze)

---

## 0.1 Goal (Why we are building this)
Build a personal, portfolio-ready resume screening tool that lets me paste/upload:
- A Job Description (JD)
- My Resume (PDF/DOCX/TXT)

…and receive:
- Overall match score + dimension breakdown
- Evidence-backed citations from JD and Resume
- Skill gaps, missing keywords, and seniority mismatch signals
- ATS-style improvement recommendations (including bullet rewrites)
- Role-specific interview questions (easy → hard) tagged by skill area + expected signals

This is a personal tool (job seeker use), but engineered using enterprise-grade practices:
- reproducible runs
- explainability (citations)
- logging + prompt versioning
- modular architecture
- evaluation plan

---

## 0.2 Scope (In / Out)
### In Scope
- Single JD + single resume (MVP), extensible to multiple resumes
- Multi-agent flow: Extractor → Scorer → Gap → InterviewQ
- RAG over JD (and optional RAG over rubric/scoring guidelines)
- Evidence + citations per rubric dimension
- Run logging (inputs hash, outputs, prompts, token usage, model, timestamps)
- UI: Streamlit dashboard + API: FastAPI

### Out of Scope (Phase 0 decision)
- ATS integration (Greenhouse/Lever)
- Hiring automation for organizations
- Automatic job scraping / auto-apply
- Fine-tuning models (use prompting + evals first)

---

## 0.3 Users & Success Metrics
### Primary user
- Me (job seeker) optimizing resume per JD

### Success Metrics
- **Explainability:** every scored dimension returns citations from JD and Resume
- **Consistency:** stable score within a small variance given same inputs
- **Actionability:** tool produces specific gaps + bullet-level rewrites
- **Time to result:** target < 30–60 seconds per JD/resume on typical configuration
- **Traceability:** each run stored with artifacts + token usage + prompt versions

---

## 0.4 Architecture Freeze (Target Design Locked)
### Pipeline
1) Ingest: JD + Resume(s) (PDF/DOCX/TXT)
2) Parse → Normalize → structured JSON with provenance
3) RAG:
   - JD embeddings → vector store
   - Rubric/guidelines embeddings → vector store (optional but strong)
4) Agents (LangChain/LangGraph):
   - Extractor Agent → candidate JSON
   - Matcher/Scorer Agent → rubric scoring + citations
   - Gap Agent → missing skills/keywords + seniority mismatch
   - InterviewQ Agent → questions + expected signals
5) Outputs: score + breakdown + evidence + gaps + interview Qs
6) Storage/Logs: SQLite/Postgres (runs + prompts + token usage + decisions)

---

## 0.5 Acceptance Criteria (Phase 0)
- [ ] A written PRD-like scope & architecture exists (this file)
- [ ] Clear rubric dimensions & output format defined
- [ ] Plan includes logging + explainability requirements
- [ ] Repo structure planned for phases 1–3

---

## 0.6 Files Created/Used in This Phase
> Phase 0 is mostly documentation + scaffolding.



### Python (planning scaffolds / placeholders)
- `apps/core/config.py` (env + settings plan)
- `apps/core/constants.py` (enums: source=JD/RESUME/RUBRIC, etc.)
- `apps/core/schemas.py` (initial Pydantic schemas drafts)
