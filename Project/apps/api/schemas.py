from __future__ import annotations
from typing import List, Optional, Literal
from pydantic import BaseModel, Field


class ProvenanceSpan(BaseModel):
    source: Literal["JD", "RESUME"]
    section: str
    start_char: int = Field(ge=0)
    end_char: int = Field(ge=0)
    quote: str = Field(max_length=200)  # enforced later to <= 20 words


class SkillItem(BaseModel):
    name: str
    provenance: Optional[ProvenanceSpan] = None


class ExperienceBullet(BaseModel):
    text: str
    provenance: Optional[ProvenanceSpan] = None


class ExperienceItem(BaseModel):
    company: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    bullets: List[ExperienceBullet] = []


class ProjectItem(BaseModel):
    name: Optional[str] = None
    tech_stack: List[str] = []
    bullets: List[ExperienceBullet] = []


class EducationItem(BaseModel):
    school: Optional[str] = None
    degree: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None


class CandidateProfile(BaseModel):
    headline: Optional[str] = None
    skills: List[SkillItem] = []
    tools: List[SkillItem] = []
    cloud: List[SkillItem] = []
    ml: List[SkillItem] = []
    llm_genai: List[SkillItem] = []
    experience: List[ExperienceItem] = []
    projects: List[ProjectItem] = []
    education: List[EducationItem] = []
    certifications: List[str] = []


class JDRequirement(BaseModel):
    text: str
    provenance: Optional[ProvenanceSpan] = None


class ParsedJD(BaseModel):
    role_title: Optional[str] = None
    must_have: List[JDRequirement] = []
    nice_to_have: List[JDRequirement] = []
    responsibilities: List[JDRequirement] = []
    keywords: List[str] = []
