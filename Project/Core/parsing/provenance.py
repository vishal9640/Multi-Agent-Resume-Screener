from __future__ import annotations
from dataclasses import dataclass
from typing import Optional


"""Small helpers for producing short previews and locating substrings.

These functions are intentionally tiny and defensive: they handle empty
inputs and perform case-insensitive search for convenience.
"""


def quote_20_words(text: str) -> str:
    """Return a short preview consisting of the first 20 words of `text`.

    - Strips leading/trailing whitespace, splits on any whitespace, then
      joins up to 20 words with single spaces.
    - Useful for creating short summaries or previews for display.
    """
    # Remove surrounding whitespace and split on whitespace into words
    words = text.strip().split()
    # Return the first 20 words joined by single spaces (safe if fewer words)
    return " ".join(words[:20])


def find_span(haystack: str, needle: str, fallback_start: int = 0):
    """Find the (start, end) indices of `needle` inside `haystack`.

    - The search is case-insensitive: both strings are compared in lower case.
    - If `needle` or `haystack` is empty, or if `needle` is not found, the
      function returns the zero-length fallback span `(fallback_start, fallback_start)`.
    - When found, `end` is `start + len(needle)` (end is exclusive, like Python slices).
    """
    # If either string is empty, we cannot find a span — return the fallback
    if not needle or not haystack:
        return (fallback_start, fallback_start)

    # Do a case-insensitive search
    idx = haystack.lower().find(needle.lower())
    if idx == -1:
        # Not found -> return fallback zero-length span
        return (fallback_start, fallback_start)
    # Found -> return (start, exclusive_end)
    return (idx, idx + len(needle))
