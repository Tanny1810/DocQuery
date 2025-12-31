import faiss
import numpy as np
from pathlib import Path

VECTOR_DIM = 384  # MiniLM embedding size
INDEX_PATH = Path("/tmp/faiss.index")

# Load or create index
if INDEX_PATH.exists():
    index = faiss.read_index(str(INDEX_PATH))
else:
    index = faiss.IndexFlatL2(VECTOR_DIM)


def store_embeddings(embeddings: list[list[float]]):
    vectors = np.array(embeddings).astype("float32")
    start_index = index.ntotal
    index.add(vectors)
    faiss.write_index(index, str(INDEX_PATH))
    return [start_index + i for i in range(len(embeddings))]


def get_vector_count() -> int:
    return index.ntotal
