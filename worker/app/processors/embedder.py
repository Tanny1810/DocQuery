from sentence_transformers import SentenceTransformer

# Load once (VERY IMPORTANT)
_model = SentenceTransformer("all-MiniLM-L6-v2")


def embed_chunks(chunks: list[str]) -> list[list[float]]:
    embeddings = _model.encode(chunks, convert_to_numpy=True, show_progress_bar=True)
    return embeddings.tolist()
