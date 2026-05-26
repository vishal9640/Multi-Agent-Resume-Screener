import json
from apps.api.db import get_conn

def log_stage(run_id: str, stage: str, payload: dict):
    conn = get_conn()
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO resume.run_logs (run_id, stage, payload)
                    VALUES (%s, %s, %s::jsonb)
                    """,
                    (run_id, stage, json.dumps(payload)),
                )
    finally:
        conn.close()
