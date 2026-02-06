from __future__ import annotations
import re #Python's built-in Regular Expression library for pattern matching and text manipulation
from typing import Dict, List, Tuple, Optional


SECTION_PATTERNS = {
    "summary": re.compile(r"^\s*(summary|professional summary|objective)\s*$", re.I), #Here re is used to compile a regular expression pattern that matches lines indicating a summary section in a resume.
    "skills": re.compile(r"^\s*(skills|technical skills|core skills)\s*$", re.I), #re.I is the same as re.IGNORECASE: makes regex matching case-insensitive.
    "experience": re.compile(r"^\s*(experience|work experience|employment|professional experience)\s*$", re.I),
    "projects": re.compile(r"^\s*(projects|project experience)\s*$", re.I),
    "education": re.compile(r"^\s*(education)\s*$", re.I),
    "certifications": re.compile(r"^\s*(certifications|certificates)\s*$", re.I),
}


def _find_section_headers(lines: List[str]) -> List[Tuple[int, str]]:
    headers = []
    for idx, line in enumerate(lines):
        clean = line.strip()
        if not clean:
            continue
        for name, pat in SECTION_PATTERNS.items():
            if pat.match(clean):
                headers.append((idx, name))
                break
    return headers


def split_resume_sections(text: str) -> Dict[str, dict]:
    """
    Returns dict:
      section_name -> { "text": str, "start_char": int, "end_char": int }
    Uses line scanning and maps back to char offsets.
    """
    if not text:
        return {"unknown": {"text": "", "start_char": 0, "end_char": 0}}

    lines = text.splitlines()
    headers = _find_section_headers(lines)

    if not headers:
        # fallback: entire text as unknown
        return {"unknown": {"text": text, "start_char": 0, "end_char": len(text)}}

    # Map line index -> char offset
    # Build cumulative char offsets per line start
    offsets = []
    running = 0
    for ln in lines:
        offsets.append(running)
        running += len(ln) + 1  # +1 newline

    sections: Dict[str, dict] = {}
    for i, (line_idx, sec_name) in enumerate(headers):
        start_line = line_idx + 1
        end_line = headers[i + 1][0] if i + 1 < len(headers) else len(lines)

        start_char = offsets[start_line] if start_line < len(offsets) else len(text)
        end_char = offsets[end_line] if end_line < len(offsets) else len(text)

        sec_text = "\n".join(lines[start_line:end_line]).strip()
        sections[sec_name] = {
            "text": sec_text,
            "start_char": start_char,
            "end_char": end_char,
        }

    return sections
