from fastapi import APIRouter, HTTPException, Query
import traceback
from Core.scoring.graph import build_graph

router = APIRouter(prefix="/score", tags=["score"])
graph = build_graph()

@router.post("/{run_id}")
def score_run(
    run_id: str,
    mode: str = Query("fast", pattern="^(fast|full)$"),
):
    """
    fast: dimension scoring + aggregate only
    full: fast + gaps + rewrites + interview questions
    """
    try:
        state = graph.invoke({"run_id": run_id, "mode": mode})
        return state["final_output"]  # we'll set this in the graph
    except Exception:
        print("❌ /score crashed:")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail="Score pipeline crashed. Check API logs.")
