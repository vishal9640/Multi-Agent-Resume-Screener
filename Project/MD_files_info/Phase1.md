# Phase 1 – Requirements Discovery

## Objective
Clearly define *what* the system must do and *why*, before designing *how*.

This phase mirrors an MNC discovery phase involving product, engineering,
and user (job seeker) alignment.

---

## A. Job Search Context

### Target Roles
- AI Engineer
- Machine Learning Engineer
- Data Scientist
- MLOps Engineer

### Experience Level
- Student / Early Career (0–2 years)
- System must support seniority inference

### Primary Goals (Priority Ordered)
1. Resume scoring vs JD
2. Resume improvement suggestions
3. Interview preparation

---

## B. Inputs & Usage

### Supported Inputs
- Resume formats: PDF, DOCX, TXT
- Job Description: pasted text or uploaded file

### Usage Pattern
- Same resume evaluated against multiple JDs
- Iterative resume versions (v1, v2, v3)

---

## C. Scoring Expectations

### Scoring Outputs
- Overall score (0–100)
- Dimension-level scores:
  - Skills
  - Experience
  - Projects
  - Education
  - Tools/Technologies

### Scoring Strictness
- Recruiter-level realism
- Evidence required for every score

### Hard Filters (Optional)
- Missing must-have skills
- Experience threshold mismatch

---

## D. Resume Improvement Loop

### Required Capabilities
- Identify missing keywords (ATS-focused)
- Suggest rewritten resume bullets
- Highlight weak or vague experience
- Track improvement across iterations

---

## E. Interview Preparation

### Question Generation
- Based on JD + resume
- Difficulty: Easy → Medium → Hard

### Signals
- Each question tagged with:
  - Skill area
  - What interviewer is evaluating

---

## F. Constraints & Assumptions

### Deployment
- local deployment

### Data Storage
- Postgres
- Encrypted or local-only (configurable)

### Assumptions
- [ASSUMPTION] Resume language is English
- [ASSUMPTION] User consents to resume processing
