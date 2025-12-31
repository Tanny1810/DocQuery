from shared.vector_store.faiss_index import FaissIndex

faiss_index = FaissIndex()


def store_embeddings(embeddings: list[list[float]]) -> list[int]:
    return faiss_index.add(embeddings)


def get_vector_count() -> int:
    return faiss_index.count()
