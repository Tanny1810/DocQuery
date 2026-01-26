from typing import Dict, List


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


def chunk_pages(
    pages: List[Dict],
    chunk_size: int = 650,
    overlap: int = 125,
) -> List[Dict]:
    chunks = []
    global_chunk_index = 0

    for page in pages:
        text = page.get("text")
        page_number = page.get("page_number")

        if not text or not text.strip():
            continue

        page_chunks = chunk_text(
            text,
            chunk_size=chunk_size,
            overlap=overlap,
        )

        for chunk in page_chunks:
            chunks.append(
                {
                    "content": chunk,
                    "page_number": page_number,
                    "chunk_index": global_chunk_index,
                }
            )
            global_chunk_index += 1

    return chunks
