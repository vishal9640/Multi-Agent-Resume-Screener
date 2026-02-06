# Phase 2 – Functional Specification

## Objective
Define **what the system does end-to-end**, independent of implementation.

---

## High-Level Workflow

1. User uploads/pastes Resume and Job Description
2. System parses and normalizes both inputs
3. RAG pipeline indexes JD and rubric
4. Agents process data sequentially
5. System generates scores, explanations, gaps, and questions
6. Results are displayed and stored

---

## Core Functional Modules

### 1. Ingestion Module
- Accepts Resume and JD
- Supports PDF/DOCX/TXT
- Extracts raw text

### 2. Parsing & Normalization
- Converts raw text → structured JSON
- Fields extracted:
  - Skills
  - Experience
  - Education
  - Projects
  - Tools
  - Bullet points
- Maintains provenance (text span mapping)

### 3. Scoring Rubric
- Configurable rubric dimensions
- Weighted scoring
- Rubric stored as structured JSON

### 4. Multi-Agent Processing

#### Extractor Agent
- Produces candidate profile JSON
- No scoring logic

#### Matcher / Scorer Agent
- Scores each rubric dimension
- Uses RAG for grounding
- Produces citations

#### Gap Agent
- Identifies missing skills
- Detects seniority mismatch
- Generates improvement actions

#### Interview Question Agent
- Generates role-specific questions
- Difficulty-tagged
- Skill-mapped

---

## Output Specifications

### Outputs Generated
- Overall score
- Dimension-wise breakdown
- Evidence citations
- Gap analysis
- Resume improvement suggestions
- Interview questions

### Output Format
- UI-rendered dashboard
- JSON export (optional)

---

## Logging & Observability

### Stored Per Run
- Input hashes
- Agent outputs
- Prompt versions
- Token usage
- Model versions
- Timestamp

---

## Acceptance Criteria
- Every score has citations
- No hallucinated claims
- Repeatable scoring given same inputs
