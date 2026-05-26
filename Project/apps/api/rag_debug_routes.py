from fastapi import APIRouter
from Core.RAG.chroma_store import debug_peek

router = APIRouter(prefix="/rag_debug", tags=["rag_debug"])

@router.get("/peek")
def peek():
    return {
        "jd_chunks": debug_peek("jd_chunks", n=5),
        "resume_chunks": debug_peek("resume_chunks", n=5),
    }
