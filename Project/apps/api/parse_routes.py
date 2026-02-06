from fastapi import APIRouter, HTTPException
from apps.api.db import get_conn
from apps.api.schemas import CandidateProfile, ParsedJD
from Core.parsing.sectionizer import split_resume_sections
from Core.parsing.resume_profile import build_candidate_profile
from Core.parsing.JD_parser import parse_jd

router = APIRouter(prefix="/parse", tags=["parse"])


@router.post("/{run_id}")
def parse_run(run_id: str):
    conn = get_conn()
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT doc_type, text_content
                    FROM resume.documents
                    WHERE run_id = %s
                    """,
                    (run_id,),
                )
                rows = cur.fetchall()

        if not rows:
            raise HTTPException(status_code=404, detail="No documents found for run_id")

        jd_text = None
        resume_text = None
        for r in rows:
            if r["doc_type"] == "JD":
                jd_text = r["text_content"]
            elif r["doc_type"] == "RESUME":
                resume_text = r["text_content"]

        if not jd_text or not resume_text:
            raise HTTPException(status_code=400, detail="JD or Resume text missing for this run")

        # Resume: sectionize + build profile
        sections = split_resume_sections(resume_text)
        candidate = build_candidate_profile(resume_text, sections)

        # JD parse
        parsed_jd = parse_jd(jd_text)

        # Validate with strict schemas (this is important for interview-grade)
        candidate_obj = CandidateProfile.model_validate(candidate)
        parsed_jd_obj = ParsedJD.model_validate(parsed_jd)

        return {
            "run_id": run_id,
            "parsed_jd": parsed_jd_obj.model_dump(),
            "candidate_profile": candidate_obj.model_dump(),
            "resume_sections": sections,
        }
    finally:
        conn.close()
