def chunk_text(
    text: str,
    chunk_size: int = 650,
    overlap: int = 125,
) -> list[str]:
    chunks = []
    start = 0
    length = len(text)

    while start < length:
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start = end - overlap

    return chunks
