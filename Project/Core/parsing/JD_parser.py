#Adding a simple JD parser + Resume profile builder

from __future__ import annotations
import re
from typing import Dict, List, Tuple

from .provenance import find_span, quote_20_words #Provenance here means “where did this extracted bullet come from".


REQ_HEADERS = [
    ("must_have", re.compile(r"(must have|required|requirements)", re.I)),
    ("nice_to_have", re.compile(r"(nice to have|preferred|good to have)", re.I)),
    ("responsibilities", re.compile(r"(responsibilities|role|what you will do|duties)", re.I)),
]


def parse_jd(text: str) -> Dict:
    """
    Heuristic JD parsing for Phase 2.
    Phase 3+ RAG will make this stronger.
    """
    out = {
        "role_title": None,
        "must_have": [],
        "nice_to_have": [],
        "responsibilities": [],
        "keywords": [],
    }

    if not text:
        return out

    # crude role title guess: first non-empty line
    for line in text.splitlines():
        if line.strip():
            out["role_title"] = line.strip()[:120]
            break

    lower = text.lower()

    # Split by headers if present
    sections = {"must_have": "", "nice_to_have": "", "responsibilities": ""}
    current = None
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped:
            continue

        matched = False
        for name, pat in REQ_HEADERS:
            if pat.search(stripped):
                current = name
                matched = True
                break
        if matched:
            continue

        if current:
            sections[current] += stripped + "\n"

    def bulletize(block: str) -> List[str]:
        bullets = []
        for ln in block.splitlines():
            ln = ln.strip("-•* \t").strip()
            if len(ln) >= 3:
                bullets.append(ln)
        return bullets[:30]

    for sec in ["must_have", "nice_to_have", "responsibilities"]:
        for item in bulletize(sections[sec]):
            s, e = find_span(text, item)
            out[sec].append({
                "text": item,
                "provenance": {
                    "source": "JD",
                    "section": sec,
                    "start_char": s,
                    "end_char": e,
                    "quote": quote_20_words(item),
                }
            })

    # Keywords: simple token pull (Phase 2)
    # You’ll improve with RAG in Phase 3.
    tokens = re.findall(r"[A-Za-z][A-Za-z0-9\-\+\.]{1,}", text)
    common_stop = set(["and","the","with","for","you","will","are","this","that","from","our","your"])
    keywords = []
    for t in tokens:
        tl = t.lower()
        if tl in common_stop:
            continue
        if len(t) <= 2:
            continue
        keywords.append(t)
    # keep unique order
    seen = set()
    uniq = []
    for k in keywords:
        kl = k.lower()
        if kl not in seen:
            uniq.append(k)
            seen.add(kl)
    out["keywords"] = uniq[:50]

    return out
