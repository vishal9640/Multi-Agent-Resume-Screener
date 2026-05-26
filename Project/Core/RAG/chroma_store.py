from __future__ import annotations
from pathlib import Path
from typing import List, Dict
import os
import chromadb
from chromadb.config import Settings

_client = None #Here we are initializing a global variable _client to None. This variable will hold the instance of the ChromaDB client once it is created.

def get_chroma_client():
    global _client
    chroma_dir = os.getenv("CHROMA_DIR", "./data/chroma")
    chroma_dir = str(Path(chroma_dir).expanduser().resolve())

    if _client is None:
        print("✅ CHROMA_DIR used by API =", chroma_dir)  # <-- critical debug
        _client = chromadb.PersistentClient(
            path=chroma_dir,
            settings=Settings(anonymized_telemetry=False)
        )
    return _client
def get_or_create_collection(name: str):
    client = get_chroma_client()
    return client.get_or_create_collection(name=name)

def debug_peek(collection_name: str, n: int = 5):
    col = get_or_create_collection(collection_name)
    data = col.get(include=["metadatas", "documents"], limit=n)
    return {
        "collection": collection_name,
        "count": col.count(),
        "sample_ids": data.get("ids", [])[:n],
        "sample_metadatas": data.get("metadatas", [])[:n],
        "sample_docs_preview": [(d[:120] + "…") if d else "" for d in data.get("documents", [])[:n]],
    }


def upsert_chunks(collection_name: str, chunks: List[Dict], embeddings: List[List[float]]):
    """
    Upsert into Chroma:
    - ids: chunk_id
    - documents: chunk text
    - metadatas: run_id, source, section, offsets
    """
    col = get_or_create_collection(collection_name)
    ids = [c["chunk_id"] for c in chunks]
    docs = [c["text"] for c in chunks]
    metas = [{
        "run_id": str(c["run_id"]),
        "source": c["source"],
        "section": c["section"],
        "start_char": c["start_char"],
        "end_char": c["end_char"],
        "hash": c.get("hash", None),
    } for c in chunks]
    col.upsert(ids=ids, documents=docs, embeddings=embeddings, metadatas=metas)

def query_chunks(collection_name: str, query_embedding: List[float], run_id: str, top_k: int = 5):
    col = get_or_create_collection(collection_name)
    res = col.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        where={"run_id": str(run_id)},
        include=["documents", "metadatas", "distances"]
    )
    # unpack first (only one query)
    out = []
    ids = res.get("ids", [[]])[0]
    docs = res.get("documents", [[]])[0]
    metas = res.get("metadatas", [[]])[0]
    dists = res.get("distances", [[]])[0]
    for i in range(len(ids)):
        out.append({
            "chunk_id": ids[i],
            "text": docs[i],
            "metadata": metas[i],
            "distance": dists[i],
        })
    return out

