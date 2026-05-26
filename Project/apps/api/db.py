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
            cur.execute("SELECT 1 FROM resume.runs WHERE run_id = %s", (run_id,))
            if not cur.fetchone():
                raise ValueError(f"Run not found: {run_id}")

            cur.execute(
                """
                SELECT DISTINCT ON (doc_type) doc_type, text_content
                FROM resume.documents
                WHERE run_id = %s AND doc_type IN ('JD', 'RESUME')
                ORDER BY doc_type, created_at DESC
                """,
                (run_id,),
            )
            rows = {r["doc_type"]: (r["text_content"] or "") for r in cur.fetchall()}
            return rows.get("JD", ""), rows.get("RESUME", "")
    finally:
        conn.close()
