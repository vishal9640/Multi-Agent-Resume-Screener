# Phase 1: Requirements Discovery & Functional Specification

## Objective
Translate the problem statement into concrete, testable functional requirements
using an MNC-style discovery process.

---

## Functional Requirements

### Inputs
- Job Description (PDF / DOCX / TXT)
- Resume (PDF / DOCX / TXT)
- Support repeated comparisons across multiple JDs

### Core Features
1. Resume scoring against JD
2. Dimension-wise breakdown (skills, experience, projects, education)
3. Evidence-backed explanations with citations
4. Skill gap and keyword gap analysis
5. Resume improvement suggestions
6. Interview question generation (easy → hard)
7. Iterative improvement tracking

---

## Scoring Requirements
- Overall score: 0–100
- Section-wise scores
- Configurable strictness:
  - Recruiter-level
  - Aspirational
  - Improvement-focused

---

## Explainability Requirements
- Every score must reference:
  - JD evidence
  - Resume evidence
- Citations must include:
  - chunk_id
  - short quoted text
  - relevance note

---

## Output Formats
- On-screen dashboard (Streamlit)
- Structured JSON outputs (for extensibility)

---

## Constraints
- No auto-rejection without explanation
- Deterministic rubric-driven scoring
- No hallucinated skills

---

## Deliverables
- Functional spec aligned with job-seeker value
- Clear acceptance criteria per feature

---

## Files Created in Phase 1
- `PHASE_1_REQUIREMENTS_DISCOVERY.md`

