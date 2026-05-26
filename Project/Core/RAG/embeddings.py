from __future__ import annotations
from typing import List
import os
import requests

def embed_texts(texts: List[str]) -> List[List[float]]:
    """
    Embeds a list of texts using Ollama embeddings API.
    """
    base = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    # nomic-embed-text: Open-source embedding model (~137M params) that converts text to 768-dim vectors
    # Runs locally via Ollama for fast, offline semantic embeddings
    model = os.getenv("OLLAMA_EMBED_MODEL", "nomic-embed-text")

    vectors: List[List[float]] = []
    for t in texts:
        payload = {"model": model, "prompt": t}
        r = requests.post(f"{base}/api/embeddings", json=payload, timeout=60) #Here it is using the requests library to send a POST request to the Ollama embeddings API endpoint with the specified model and text prompt.
        r.raise_for_status()
        data = r.json()
        vec = data.get("embedding")
        if not vec:
            raise RuntimeError("No embedding returned from Ollama.")
        vectors.append(vec)
    return vectors
