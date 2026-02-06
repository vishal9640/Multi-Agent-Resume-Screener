import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

load_dotenv()

def get_conn():
    return psycopg2.connect(
        host=os.getenv("POSTGRES_HOST", "localhost"),
        port=int(os.getenv("POSTGRES_PORT", "5432")),
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        cursor_factory=RealDictCursor,
    )
def get_run_texts(run_id: str):
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            # confirm run exists (optional)
            cur.execute("SELECT 1 FROM resume.runs WHERE run_id = %s", (run_id,))
            if not cur.fetchone():
                raise ValueError(f"Run not found: {run_id}")

            # JD
            cur.execute(
                """
                SELECT text_content
                FROM resume.documents
                WHERE run_id = %s AND doc_type = 'JD'
                ORDER BY created_at DESC
                LIMIT 1
                """,
                (run_id,),
            )
            jd_row = cur.fetchone()
            jd_text = (jd_row["text_content"] if jd_row else "") or ""

            # RESUME
            cur.execute(
                """
                SELECT text_content
                FROM resume.documents
                WHERE run_id = %s AND doc_type = 'RESUME'
                ORDER BY created_at DESC
                LIMIT 1
                """,
                (run_id,),
            )
            res_row = cur.fetchone()
            resume_text = (res_row["text_content"] if res_row else "") or ""

            return jd_text, resume_text
    finally:
        conn.close()
