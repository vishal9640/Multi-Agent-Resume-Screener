from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from typing import Optional, List, Dict, Any
from datetime import datetime
import os

from apps.api.parse_routes import router as parse_router
from apps.api.rag_routes import router as rag_router
from apps.api.rag_debug_routes import router as rag_debug_router
from apps.api.score_routes import router as score_router

from Core.parsing.doc_extractor import (
    extract_text_from_pdf_bytes,
    extract_text_from_docx_bytes,
    save_upload_bytes,
)
from apps.api.db import get_conn
from apps.api.utils import sha256_text, safe_decode_bytes

app = FastAPI(title="Personal Resume Analyzer API v0.1")
app.include_router(parse_router)
app.include_router(rag_router)
app.include_router(rag_debug_router)
app.include_router(score_router)

# Maximum allowed characters for text input to prevent memory issues
MAX_TEXT_CHARS = 2_000_000


def _normalize_text_input(
    pasted_text: Optional[str],
    upload: Optional[UploadFile],
    label: str,
    run_id_for_artifacts: str,
) -> Dict[str, Any]:
    """Use pasted text if provided, otherwise extract from uploaded PDF/DOCX/TXT."""
    artifact_dir = os.getenv("ARTIFACT_DIR", "./data/artifacts")

    if pasted_text and pasted_text.strip():
        text = pasted_text.strip()
        if len(text) > MAX_TEXT_CHARS:
            raise HTTPException(status_code=413, detail=f"{label} pasted text too large.")
        return {
            "text": text,
            "file_name": None,
            "mime_type": "text/plain",
            "source": "pasted",
            "file_path": None,
            "parse_quality": "OK",
        }

    if upload is None:
        raise HTTPException(status_code=400, detail=f"{label} is required (paste text or upload file).")

    file_name = upload.filename
    mime_type = upload.content_type or "application/octet-stream"
    raw = upload.file.read()

    file_path = save_upload_bytes(artifact_dir, run_id_for_artifacts, label.upper(), file_name or "upload.bin", raw)

    if mime_type == "text/plain" or (file_name and file_name.lower().endswith(".txt")):
        text = safe_decode_bytes(raw).strip()
        quality = "OK" if len(text) >= 200 else "LOW_QUALITY"
    elif (file_name and file_name.lower().endswith(".pdf")) or mime_type == "application/pdf":
        text, quality = extract_text_from_pdf_bytes(raw)
    elif (file_name and file_name.lower().endswith(".docx")) or mime_type in (
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "application/msword",
    ):
        text, quality = extract_text_from_docx_bytes(raw)
    else:
        text = ""
        quality = "FAILED"

    if not text:
        text = f"[PARSE FAILED: {file_name} ({mime_type})]"
        quality = "FAILED"

    if len(text) > MAX_TEXT_CHARS:
        text = text[:MAX_TEXT_CHARS] + "\n[TRUNCATED]"

    return {
        "text": text,
        "file_name": file_name,
        "mime_type": mime_type,
        "source": "file",
        "file_path": file_path,
        "parse_quality": quality,
    }


@app.get("/health")
def health():
    return {"status": "ok", "time": datetime.utcnow().isoformat()}


@app.post("/ingest")
def ingest(
    jd_text: Optional[str] = Form(None),
    resume_text: Optional[str] = Form(None),
    jd_file: Optional[UploadFile] = File(None),
    resume_file: Optional[UploadFile] = File(None),
):
    conn = get_conn()
    try:
        # Create a placeholder run row first so we have a run_id for artifact naming
        with conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO resume.runs (status, jd_hash, resume_hash)
                    VALUES ('INGESTED', %s, %s)
                    RETURNING run_id, created_at, status
                    """,
                    ("TEMP", "TEMP"),
                )
                run_row = cur.fetchone()
                run_id = str(run_row["run_id"])

        jd = _normalize_text_input(jd_text, jd_file, "JD", run_id)
        res = _normalize_text_input(resume_text, resume_file, "Resume", run_id)

        jd_hash = sha256_text(jd["text"])
        resume_hash = sha256_text(res["text"])

        with conn:
            with conn.cursor() as cur:
                cur.execute(
                    "UPDATE resume.runs SET jd_hash=%s, resume_hash=%s WHERE run_id=%s",
                    (jd_hash, resume_hash, run_id),
                )
                cur.execute(
                    """
                    INSERT INTO resume.documents (run_id, doc_type, file_name, mime_type, text_content, sha256_hash, file_path, parse_quality)
                    VALUES (%s, 'JD', %s, %s, %s, %s, %s, %s)
                    """,
                    (run_id, jd["file_name"], jd["mime_type"], jd["text"], jd_hash, jd["file_path"], jd["parse_quality"]),
                )
                cur.execute(
                    """
                    INSERT INTO resume.documents (run_id, doc_type, file_name, mime_type, text_content, sha256_hash, file_path, parse_quality)
                    VALUES (%s, 'RESUME', %s, %s, %s, %s, %s, %s)
                    """,
                    (run_id, res["file_name"], res["mime_type"], res["text"], resume_hash, res["file_path"], res["parse_quality"]),
                )

        return {
            "run_id": run_id,
            "created_at": run_row["created_at"].isoformat(),
            "status": run_row["status"],
            "jd": {"hash": jd_hash, "source": jd["source"], "file_name": jd["file_name"], "mime_type": jd["mime_type"], "parse_quality": jd["parse_quality"]},
            "resume": {"hash": resume_hash, "source": res["source"], "file_name": res["file_name"], "mime_type": res["mime_type"], "parse_quality": res["parse_quality"]},
        }
    finally:
        conn.close()


@app.get("/runs")
def list_runs(limit: int = 20):
    limit = max(1, min(limit, 200))  # clamp between 1 and 200
    conn = get_conn()
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT run_id, created_at, status, jd_hash, resume_hash
                    FROM resume.runs
                    ORDER BY created_at DESC
                    LIMIT %s
                    """,
                    (limit,),
                )
                rows = cur.fetchall()

        return {
            "runs": [
                {
                    "run_id": str(r["run_id"]),
                    "created_at": r["created_at"].isoformat(),
                    "status": r["status"],
                    "jd_hash": r["jd_hash"],
                    "resume_hash": r["resume_hash"],
                }
                for r in rows
            ]
        }
    finally:
        conn.close()
