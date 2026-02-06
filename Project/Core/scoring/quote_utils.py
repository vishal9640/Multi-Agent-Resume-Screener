def quote_20_words(text: str) -> str:
    words = (text or "").strip().split()
    return " ".join(words[:20])
