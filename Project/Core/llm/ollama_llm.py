import os, requests, json

def ollama_chat(prompt: str, system: str = "", model: str = "qwen3:8b") -> dict:
    base = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    payload = {
        "model": model,
        "messages": [
            {"role":"system", "content": system},
            {"role":"user", "content": prompt},
        ],
        "stream": False
    }
    r = requests.post(f"{base}/api/chat", json=payload, timeout=500)
    r.raise_for_status()
    txt = r.json()["message"]["content"]
    return json.loads(txt)  # expect JSON-only
