SCORER_SYSTEM = """You are a strict but helpful recruiter-level resume evaluator.
You MUST use only the provided evidence chunks.
Return JSON only, no extra text."""

SCORE_DIM_PROMPT = """Score dimension: {dimension}
Weight: {weight}

Rubric:
{rubric}

JD Evidence:
{jd_evidence}

Resume Evidence:
{resume_evidence}

Return JSON:
{{
  "score": <0-100>,
  "rationale": "...",
  "jd_citations": [{{"chunk_id":"...","quote":"<=20 words","relevance":"..."}}],
  "resume_citations": [{{"chunk_id":"...","quote":"<=20 words","relevance":"..."}}]
}}
"""

GAP_PROMPT = """Given JD + resume evidence, find missing skills/keywords/seniority gaps.
Return JSON list:
[
  {"type":"SKILL|KEYWORD|SENIORITY","item":"...","suggestion":"..."}
]
"""

REWRITE_PROMPT = """Suggest resume bullet improvements (ATS + clarity).
DO NOT overwrite—propose suggestions.
Return JSON list:
[
  {"original":"...","suggested":"...","reason":"...","requires_permission": true}
]
"""

INTERVIEW_Q_PROMPT = """Generate role-specific interview questions based on JD + resume.
Return JSON list of objects:
[
  {"level":"basic|intermediate|advanced","skill_area":"...","question":"...","expected_signals":["..."]}
]
"""