from __future__ import annotations
from typing import Optional, Tuple
from pathlib import Path
from io import BytesIO

from pypdf import PdfReader
import docx


def extract_text_from_pdf_bytes(data: bytes) -> Tuple[str, str]:
    """
    Returns (text, quality) where quality is: OK / LOW_QUALITY / FAILED
    """
    try:
        reader = PdfReader(BytesIO(data))
        pages_text = []
        for p in reader.pages:
            t = p.extract_text() or ""
            pages_text.append(t)
        text = "\n".join(pages_text).strip() #strip() is used to remove characters from the start and end of a string (default: whitespace).
        if len(text) < 200:
            return (text, "LOW_QUALITY")
        return (text, "OK")
    except Exception:
        return ("", "FAILED")


def extract_text_from_docx_bytes(data: bytes) -> Tuple[str, str]:
    try:
        doc = docx.Document(BytesIO(data))
        parts = []
        for para in doc.paragraphs:
            if para.text and para.text.strip():
                parts.append(para.text.strip())
        text = "\n".join(parts).strip()
        if len(text) < 200:
            return (text, "LOW_QUALITY")
        return (text, "OK")
    except Exception:
        return ("", "FAILED")


def save_upload_bytes(artifact_dir: str, run_id: str, doc_type: str, filename: str, data: bytes) -> str:
    """
    Save uploaded file bytes for reproducibility.
    Returns file path as string.
    """
    base = Path(artifact_dir)
    base.mkdir(parents=True, exist_ok=True)
    safe_name = filename.replace("/", "_").replace("\\", "_")
    path = base / f"{run_id}_{doc_type}_{safe_name}"
    path.write_bytes(data)
    return str(path)
