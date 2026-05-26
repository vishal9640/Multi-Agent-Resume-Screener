from __future__ import annotations
from typing import List, Literal, Optional
from pydantic import BaseModel, Field

class Citation(BaseModel):
    source: Literal["JD", "RESUME"]
    chunk_id: str
    quote: str = Field(max_length=200)  # we enforce <=20 words in code
    relevance: str

class DimensionScore(BaseModel):
    dimension: str
    score: int = Field(ge=0, le=100)
    weight: float = Field(ge=0, le=1)
    rationale: str
    jd_citations: List[Citation] = []
    resume_citations: List[Citation] = []

class HardFlag(BaseModel):
    type: Literal["MUST_HAVE_MISSING", "SENIORITY_MISMATCH", "OTHER"]
    message: str

class GapItem(BaseModel):
    type: Literal["SKILL", "KEYWORD", "SENIORITY"]
    item: str
    suggestion: str

class RewriteSuggestion(BaseModel):
    original: str
    suggested: str
    reason: str
    requires_permission: bool = True

class InterviewQuestion(BaseModel):
    level: Literal["basic", "intermediate", "advanced"]
    skill_area: str
    question: str
    expected_signals: List[str] = []

class ScoreOutput(BaseModel):
    run_id: str
    overall_score: int = Field(ge=0, le=100)
    decision: Literal["strong_match", "match", "weak_match", "no_match"]
    hard_reject: bool = False
    hard_flags: List[HardFlag] = []
    dimension_scores: List[DimensionScore] = []
    gaps: List[GapItem] = []
    rewrites: List[RewriteSuggestion] = []
    interview_questions: List[InterviewQuestion] = []
