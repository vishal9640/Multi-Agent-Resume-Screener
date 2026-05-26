# PHASE 3 — Agentic Workflow (LangGraph) + Scoring + Citations + Logging
**Project:** Personal Multi-Agent Resume Analyzer (LLM + RAG)  
**Phase:** 3 (Agents, orchestration, outputs, run logs, UI wiring)  
**Status:** Completed (as per architecture plan)

---

## 3.1 Objective
Build the multi-agent system using LangGraph:
- Extractor Agent → Candidate Profile JSON
- Matcher/Scorer Agent → rubric-based scoring + citations from JD + Resume
- Gap Agent → missing skills + keywords + seniority mismatch + fixes
- InterviewQ Agent → questions easy→hard + expected signals
- Persist run logs (prompts, decisions, token usage)
- Produce final output object for Streamlit UI + API response

---

## 3.2 LangGraph Orchestration (State Machine)
### Global State Object
- `run_id`
- `jd_text`, `resume_text`
- `jd_chunks[]`, `resume_chunks[]`, `rubric_chunks[]`
- `candidate_profile`
- `scores` (overall + dimension-wise)
- `citations` (per dimension)
- `gaps` (skills/keywords/seniority)
- `recommendations` (resume edits + bullet rewrites)
- `interview_questions[]`
- `run_logs` (token usage, prompts, model versions)

### Nodes (graph)
1) `parse_inputs_node`
2) `extractor_agent_node`
3) `scorer_agent_node`
4) `gap_agent_node`
5) `interviewq_agent_node`
6) `finalize_output_node`
7) `persist_run_node`

---

## 3.3 Scoring Strategy (Rubric-driven)
- Score per dimension:
  - Skills match
  - Relevant experience alignment
  - Project relevance
  - Tools/stack alignment
  - Seniority alignment
  - Domain match
- Provide:
  - numeric score
  - rationale
  - citations from JD + Resume
  - confidence estimate (optional)

---

## 3.4 Citation Format (Hard Requirement)
Each dimension output must include:
- `jd_citations[]`: `{chunk_id, quote<=20 words, relevance_note}`
- `resume_citations[]`: `{chunk_id, quote<=20 words, relevance_note}`

Quotes should be short to keep UI readable.

---

## 3.5 Run Logging (SQLite/Postgres)
Persist each run:
- inputs hash
- model + embedding model
- prompts per agent + prompt version
- token usage per agent
- outputs (scores/gaps/questions)
- timestamps

---

## 3.6 Outputs (Final Contract)
- `overall_score`
- `dimension_scores[]`
- `citations` (by dimension)
- `gaps`
- `recommendations` (ATS keywords + bullet rewrites)
- `interview_questions[]` (tagged, easy→hard, expected signals)
- `run_metadata`

---

## 3.7 Acceptance Criteria (Phase 3)
- [ ] LangGraph executes full workflow end-to-end
- [ ] Each rubric dimension returns JD + Resume citations
- [ ] Gap analysis lists missing skills + keywords + seniority mismatch
- [ ] Interview Q generation works and tags by skill area
- [ ] Each run is saved to DB with prompts + token usage

---

## 3.8 Python Files Implemented in This Phase
### Agents
- `apps/agents/extractor_agent.py`
- `apps/agents/scorer_agent.py`
- `apps/agents/gap_agent.py`
- `apps/agents/interviewq_agent.py`

### Prompts (versioned)
- `apps/prompts/extractor_prompts.py`
- `apps/prompts/scorer_prompts.py`
- `apps/prompts/gap_prompts.py`
- `apps/prompts/interview_prompts.py`

### Orchestration (LangGraph)
- `apps/workflows/state.py`
- `apps/workflows/graph.py`
- `apps/workflows/nodes.py`

### Logging / DB
- `apps/db/connection.py`
- `apps/db/models.py`
- `apps/db/repositories/runs_repo.py`
- `apps/db/repositories/chunks_repo.py`
- `apps/db/repositories/prompts_repo.py`

### API + UI integration
- `apps/api/routes/analyze.py`
- `apps/ui/streamlit_app.py`
