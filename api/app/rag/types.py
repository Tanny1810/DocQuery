from typing import TypedDict, List


class RetrievedChunkDebug(TypedDict):
    document_id: str
    chunk_index: int
    distance: float


class RAGDebugMetadata(TypedDict):
    retrieved_chunks: List[RetrievedChunkDebug]
    retrieved_count: int
    used_in_prompt: int
    prompt_length: int
    fallback_used: bool
