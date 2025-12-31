import faiss
import numpy as np
from pathlib import Path

VECTOR_DIM = 384
INDEX_PATH = Path("/data/faiss/faiss.index")  # mounted volume


class FaissIndex:
    def __init__(self):
        if INDEX_PATH.exists():
            self.index = faiss.read_index(str(INDEX_PATH))
        else:
            self.index = faiss.IndexFlatL2(VECTOR_DIM)

    def add(self, embeddings: list[list[float]]) -> list[int]:
        vectors = np.array(embeddings, dtype="float32")
        start = self.index.ntotal
        self.index.add(vectors)
        faiss.write_index(self.index, str(INDEX_PATH))
        return [start + i for i in range(len(embeddings))]

    def search(self, query_embedding: list[float], k: int):
        vector = np.array([query_embedding], dtype="float32")
        distances, indices = self.index.search(vector, k)
        return indices[0].tolist(), distances[0].tolist()
    
    def count(self) -> int:
        return self.index.ntotal
