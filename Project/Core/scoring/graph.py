from typing import TypedDict, Any, Dict, List
from langgraph.graph import StateGraph, END

from Core.RAG.retriever import retrieve_evidence
from Core.scoring.rubric import DIMENSIONS
from Core.scoring.prompts import (
    SCORER_SYSTEM, SCORE_DIM_PROMPT, GAP_PROMPT, REWRITE_PROMPT, INTERVIEW_Q_PROMPT
)
from Core.llm.ollama_llm import ollama_chat
from Core.scoring.quote_utils import quote_20_words
from apps.api.schemas_phase4 import ScoreOutput


class ScoreState(TypedDict, total=False):
    run_id: str
    mode: str
    evidence: Dict[str, Any]
    dimension_results: List[Dict[str, Any]]
    overall_score: int
    decision: str
    hard_reject: bool
    hard_flags: List[Dict[str, Any]]
    gaps: List[Dict[str, Any]]
    rewrites: List[Dict[str, Any]]
    interview_questions: List[Dict[str, Any]]
    final_output: Dict[str, Any]


def _evidence_ctx(state: ScoreState) -> str:
    return str(state["evidence"]["dimensions"])[:6000]


def node_retrieve(state: ScoreState) -> ScoreState:
    state["evidence"] = retrieve_evidence(state["run_id"], top_k=5)
    return state


def node_score_dimensions(state: ScoreState) -> ScoreState:
    results = []
    by_dim = {d["dimension"]: d for d in state["evidence"]["dimensions"]}

    for d in DIMENSIONS:
        dim_name = d["dimension"]
        ev = by_dim.get(dim_name, {})

        jd_text = "\n".join([f'{x["chunk_id"]}: {x["snippet"]}' for x in ev.get("jd_evidence", [])])[:2500]
        res_text = "\n".join([f'{x["chunk_id"]}: {x["snippet"]}' for x in ev.get("resume_evidence", [])])[:2500]

        prompt = SCORE_DIM_PROMPT.format(
            dimension=dim_name,
            weight=d["weight"],
            rubric=d["rubric"],
            jd_evidence=jd_text,
            resume_evidence=res_text,
        )

        out = ollama_chat(prompt, system=SCORER_SYSTEM)

        for c in out.get("jd_citations", []):
            c["quote"] = quote_20_words(c.get("quote", ""))
        for c in out.get("resume_citations", []):
            c["quote"] = quote_20_words(c.get("quote", ""))

        results.append({"dimension": dim_name, "weight": d["weight"], **out})

    state["dimension_results"] = results
    return state


def node_aggregate(state: ScoreState) -> ScoreState:
    weighted = sum((r["score"] / 100.0) * r["weight"] for r in state["dimension_results"])
    overall = int(round(weighted * 100))
    state["overall_score"] = overall

    if overall >= 80:
        state["decision"] = "strong_match"
    elif overall >= 65:
        state["decision"] = "match"
    elif overall >= 45:
        state["decision"] = "weak_match"
    else:
        state["decision"] = "no_match"
    return state


def node_gaps(state: ScoreState) -> ScoreState:
    ctx = _evidence_ctx(state)
    state["gaps"] = ollama_chat(GAP_PROMPT + "\n\nCONTEXT:\n" + ctx, system=SCORER_SYSTEM)
    return state


def node_rewrites(state: ScoreState) -> ScoreState:
    ctx = _evidence_ctx(state)
    state["rewrites"] = ollama_chat(REWRITE_PROMPT + "\n\nCONTEXT:\n" + ctx, system=SCORER_SYSTEM)
    return state


def node_interview_qs(state: ScoreState) -> ScoreState:
    ctx = _evidence_ctx(state)
    state["interview_questions"] = ollama_chat(INTERVIEW_Q_PROMPT + "\n\nCONTEXT:\n" + ctx, system=SCORER_SYSTEM)
    return state


def node_finalize(state: ScoreState) -> ScoreState:
    out = {
        "run_id": state["run_id"],
        "overall_score": state["overall_score"],
        "decision": state["decision"],
        "hard_reject": state.get("hard_reject", False),
        "hard_flags": state.get("hard_flags", []),
        "dimension_scores": [
            {
                "dimension": r["dimension"],
                "score": r["score"],
                "weight": r["weight"],
                "rationale": r.get("rationale", ""),
                "jd_citations": [{"source": "JD", **c} for c in r.get("jd_citations", [])],
                "resume_citations": [{"source": "RESUME", **c} for c in r.get("resume_citations", [])],
            }
            for r in state.get("dimension_results", [])
        ],
        "gaps": state.get("gaps", []),
        "rewrites": state.get("rewrites", []),
        "interview_questions": state.get("interview_questions", []),
    }
    state["final_output"] = out
    return state


def route_after_aggregate(state: ScoreState) -> str:
    return "gaps" if state.get("mode", "fast") == "full" else "finalize"


def build_graph():
    g = StateGraph(ScoreState)
    g.add_node("retrieve", node_retrieve)
    g.add_node("score_dims", node_score_dimensions)
    g.add_node("aggregate", node_aggregate)
    g.add_node("gaps", node_gaps)
    g.add_node("rewrites", node_rewrites)
    g.add_node("interview", node_interview_qs)
    g.add_node("finalize", node_finalize)

    g.set_entry_point("retrieve")
    g.add_edge("retrieve", "score_dims")
    g.add_edge("score_dims", "aggregate")
    g.add_conditional_edges("aggregate", route_after_aggregate, {
        "gaps": "gaps",
        "finalize": "finalize",
    })
    g.add_edge("gaps", "rewrites")
    g.add_edge("rewrites", "interview")
    g.add_edge("interview", "finalize")
    g.add_edge("finalize", END)

    return g.compile()
