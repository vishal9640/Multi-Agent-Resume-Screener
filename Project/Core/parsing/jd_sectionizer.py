import re

JD_PATTERNS = {
    "summary": re.compile(r"^\s*(about the role|overview|summary)\s*:?\s*$", re.I),
    "responsibilities": re.compile(r"^\s*(responsibilities|what you.?ll do|what you will do|duties)\s*:?\s*$", re.I),
    "requirements": re.compile(r"^\s*(requirements|qualifications|what we.?re looking for|must have)\s*:?\s*$", re.I),
    "preferred": re.compile(r"^\s*(preferred qualifications|nice to have|preferred)\s*:?\s*$", re.I),
    "tech_stack": re.compile(r"^\s*(tech stack|tools|technology|stack)\s*:?\s*$", re.I),
    "benefits": re.compile(r"^\s*(benefits|perks|compensation)\s*:?\s*$", re.I),
}

def split_jd_sections(text: str):
    if not text or not text.strip():
        return {}

    lines = text.splitlines()

    offsets = []
    pos = 0
    for line in lines:
        offsets.append(pos)
        pos += len(line) + 1  # newline

    hits = []
    for i, line in enumerate(lines):
        s = line.strip()
        if not s:
            continue
        for name, pat in JD_PATTERNS.items():
            if pat.match(s):
                hits.append((offsets[i], name))
                break

    hits.sort(key=lambda x: x[0])

    # fallback: no headings -> whole JD as one section
    if not hits:
        return {"jd": {"text": text.strip(), "start_char": 0, "end_char": len(text)}}

    sections = {}
    first_pos, _ = hits[0]
    if first_pos > 0:
        sections["summary"] = {"text": text[:first_pos].strip(), "start_char": 0, "end_char": first_pos}

    for idx, (start, name) in enumerate(hits):
        end = hits[idx + 1][0] if idx + 1 < len(hits) else len(text)
        body = text[start:end].strip()
        if body:
            sections[name] = {"text": body, "start_char": start, "end_char": end}

    return sections
