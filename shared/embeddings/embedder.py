from sentence_transformers import SentenceTransformer

# Load once per process
_model = SentenceTransformer(
    "all-MiniLM-L6-v2",
    cache_folder="/app/.hf_cache",
)


def embed_text(text: str) -> list[float]:
    """
    Embed a single query string.
    """
    embedding = _model.encode(
        text,
        convert_to_numpy=True,
        show_progress_bar=False,
    )
    return embedding.tolist()


def embed_chunks(chunks: list[str]) -> list[list[float]]:
    """
    Embed multiple document chunks.
    """
    embeddings = _model.encode(
        chunks,
        convert_to_numpy=True,
        show_progress_bar=False,
    )
    return embeddings.tolist()
