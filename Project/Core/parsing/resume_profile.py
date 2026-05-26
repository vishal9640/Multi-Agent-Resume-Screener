from __future__ import annotations
import re
from typing import Dict, List

from Core.parsing.provenance import find_span, quote_20_words


def _extract_skills_from_section(section_text: str) -> List[str]:
    if not section_text:
        return []
    cleaned = section_text.replace("|", ",").replace("•", ",").replace("·", ",")
    parts = [p.strip() for p in re.split(r",|\n", cleaned) if p.strip()]
    return [p for p in parts if len(p.split()) <= 4][:60]


def _parse_bullets(raw_text: str, section_text: str, section_name: str, limit: int) -> list:
    lines = [ln.strip() for ln in section_text.splitlines() if ln.strip()]
    bullets = []
    for ln in lines[:limit]:
        b = ln.strip("-•* ").strip()
        if len(b) < 5:
            continue
        s, e = find_span(raw_text, b)
        bullets.append({
            "text": b,
            "provenance": {
                "source": "RESUME",
                "section": section_name,
                "start_char": s,
                "end_char": e,
                "quote": quote_20_words(b),
            }
        })
    return bullets


def build_candidate_profile(raw_resume_text: str, sections: Dict[str, dict]) -> Dict:
    out = {
        "headline": None,
        "skills": [],
        "tools": [],
        "cloud": [],
        "ml": [],
        "llm_genai": [],
        "experience": [],
        "projects": [],
        "education": [],
        "certifications": [],
    }

    for line in raw_resume_text.splitlines():
        if line.strip():
            out["headline"] = line.strip()[:120]
            break

    skills_sec = sections.get("skills", {}).get("text", "")
    for s in _extract_skills_from_section(skills_sec):
        start, end = find_span(raw_resume_text, s)
        out["skills"].append({
            "name": s,
            "provenance": {
                "source": "RESUME",
                "section": "skills",
                "start_char": start,
                "end_char": end,
                "quote": quote_20_words(s),
            }
        })

    proj_text = sections.get("projects", {}).get("text", "")
    if proj_text.strip():
        out["projects"].append({
            "name": "Projects (parsed)",
            "tech_stack": [],
            "bullets": _parse_bullets(raw_resume_text, proj_text, "projects", 25),
        })

    exp_text = sections.get("experience", {}).get("text", "")
    if exp_text.strip():
        out["experience"].append({
            "title": None,
            "company": None,
            "start_date": None,
            "end_date": None,
            "bullets": _parse_bullets(raw_resume_text, exp_text, "experience", 30),
        })

    return out
