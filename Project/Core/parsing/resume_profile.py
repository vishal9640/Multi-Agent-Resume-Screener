from __future__ import annotations
import re
from typing import Dict, List

from Core.parsing.provenance import find_span, quote_20_words


def _extract_skills_from_section(section_text: str) -> List[str]:
    """
    Simple skill extraction:
    - split by commas, pipes, bullets
    """
    if not section_text:
        return []
    cleaned = section_text.replace("|", ",").replace("•", ",").replace("·", ",")
    parts = [p.strip() for p in re.split(r",|\n", cleaned) if p.strip()]
    # remove obviously long sentences
    skills = [p for p in parts if len(p.split()) <= 4][:60]
    return skills


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

    # headline: first non-empty line
    for line in raw_resume_text.splitlines():
        if line.strip():
            out["headline"] = line.strip()[:120]
            break

    # skills section
    skills_sec = sections.get("skills", {}).get("text", "")
    skills = _extract_skills_from_section(skills_sec)

    for s in skills:
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

    # projects bullets (basic)
    proj_text = sections.get("projects", {}).get("text", "")
    proj_lines = [ln.strip() for ln in proj_text.splitlines() if ln.strip()]
    if proj_lines:
        # crude: group into one project object (Phase 2)
        bullets = []
        for ln in proj_lines[:25]:
            if ln.startswith(("-", "•", "*")):
                b = ln.strip("-•* ").strip()
            else:
                b = ln
            if len(b) < 5:
                continue
            s, e = find_span(raw_resume_text, b)
            bullets.append({
                "text": b,
                "provenance": {
                    "source": "RESUME",
                    "section": "projects",
                    "start_char": s,
                    "end_char": e,
                    "quote": quote_20_words(b),
                }
            })
        out["projects"].append({
            "name": "Projects (parsed)",
            "tech_stack": [],
            "bullets": bullets,
        })

    # experience bullets (basic)
    exp_text = sections.get("experience", {}).get("text", "")
    exp_lines = [ln.strip() for ln in exp_text.splitlines() if ln.strip()]
    if exp_lines:
        bullets = []
        for ln in exp_lines[:30]:
            b = ln.strip("-•* ").strip()
            if len(b) < 5:
                continue
            s, e = find_span(raw_resume_text, b)
            bullets.append({
                "text": b,
                "provenance": {
                    "source": "RESUME",
                    "section": "experience",
                    "start_char": s,
                    "end_char": e,
                    "quote": quote_20_words(b),
                }
            })
        out["experience"].append({
            "title": None,
            "company": None,
            "start_date": None,
            "end_date": None,
            "bullets": bullets
        })

    return out
