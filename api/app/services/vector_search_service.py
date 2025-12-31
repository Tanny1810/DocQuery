from shared.vector_store.faiss_index import FaissIndex
from shared.embeddings.embedder import embed_text

faiss_index = FaissIndex()


def search_similar_chunks(query: str, top_k: int, oversample: int = 3):
    query_embedding = embed_text(query)

    vector_ids, distances = faiss_index.search(
        query_embedding,
        k=top_k * oversample,
    )

    return vector_ids, distances
