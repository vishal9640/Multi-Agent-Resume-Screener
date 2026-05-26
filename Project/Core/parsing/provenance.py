from __future__ import annotations


def quote_20_words(text: str) -> str:
    words = (text or "").strip().split()
    return " ".join(words[:20])


def find_span(haystack: str, needle: str, fallback_start: int = 0):
    """Case-insensitive substring search. Returns (start, end) or (fallback_start, fallback_start) if not found."""
    if not needle or not haystack:
        return (fallback_start, fallback_start)
    idx = haystack.lower().find(needle.lower())
    if idx == -1:
        return (fallback_start, fallback_start)
    return (idx, idx + len(needle))
