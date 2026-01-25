import strawberry
from typing import List


@strawberry.type
class RetrievedChunkDebugType:
    document_id: str
    chunk_index: int
    distance: float
    rerank_score: float


@strawberry.type
class RAGDebugMetadataType:
    retrieved_chunks: List[RetrievedChunkDebugType]
    retrieved_count: int
    used_in_prompt: int
    prompt_length: int
    fallback_used: bool
