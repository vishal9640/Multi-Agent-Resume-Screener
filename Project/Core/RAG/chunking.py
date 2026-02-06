from __future__ import annotations
from typing import List, Dict, Tuple
import hashlib
import re
from typing import List, Tuple
import hashlib

BULLET_RE = re.compile(r"^\s*(•|-|\*|–|—|\d+[.)])\s+")
HEADERISH_RE = re.compile(r"^[A-Z][A-Z\s/&]{3,}$")  # e.g., "WORK EXPERIENCE"

def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8", errors="ignore")).hexdigest()

def _normalize_space(s: str) -> str:
    return " ".join(s.split())

def _split_paragraphs(text):
    blocks = []
    start = 0
    for m in re.finditer(r"\n\s*\n", text):
        end = m.start()
        block = text[start:end].strip()
        if block:
            blocks.append((start, end, block))
        start = m.end()
    if start < len(text):
        block = text[start:].strip()
        if block:
            blocks.append((start, len(text), block))
    return blocks


def _split_lines(text):
    blocks = []
    start = 0
    for m in re.finditer(r"\n", text):
        end = m.start()
        line = text[start:end].strip()
        if line:
            blocks.append((start, end, line))
        start = m.end()
    if start < len(text):
        line = text[start:].strip()
        if line:
            blocks.append((start, len(text), line))
    return blocks


def chunk_text_with_offsets(
    text: str,
    source: str,
    section: str,
    run_id: str,
    prefix: str,
    max_chars: int = 700,
    min_chars: int = 120,
):
    if not text or not text.strip():
        return []

    # 1) Try paragraph split
    blocks = _split_paragraphs(text)

    # 2) Fallback to line split (CRITICAL for resumes)
    if len(blocks) <= 1:
        blocks = _split_lines(text)

    chunks = []
    buf = []
    buf_start = None
    chunk_idx = 1

    def flush():
        nonlocal buf, buf_start, chunk_idx
        if not buf:
            return

        joined = "\n".join([b[2] for b in buf]).strip()
        if not joined:
            buf = []
            buf_start = None
            return

        start = buf_start
        end = buf[-1][1]

        chunks.append({
            "chunk_id": f"{prefix}-{chunk_idx:04d}",
            "text": joined,
            "source": source,
            "section": section,
            "run_id": run_id,
            "start_char": start,
            "end_char": end,
            "hash": sha256_text(joined),
        })

        chunk_idx += 1
        buf = []
        buf_start = None

    # 3) Accumulate blocks
    for start, end, blk in blocks:
        if buf_start is None:
            buf_start = start

        candidate = "\n".join([b[2] for b in buf] + [blk])

        # 🔑 KEY FIX:
        # Flush if:
        #  - candidate too big
        #  - OR buffer already has enough content
        if len(candidate) >= max_chars and buf:
            flush()

        buf.append((start, end, blk))

        # 🔑 KEY FIX:
        # If buffer has crossed min_chars, flush immediately
        if len("\n".join([b[2] for b in buf])) >= min_chars:
            flush()

    # 4) Final flush (FORCE)
    flush()

    return chunks
