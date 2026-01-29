from typing import TypedDict, List, Optional
from dataclasses import dataclass
from uuid import UUID


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


@dataclass(frozen=True)
class Source:
    document_id: UUID
    filename: str
    chunk_index: int
    page_number: Optional[int] = None
    section_title: Optional[str] = None
    score: float = 0.0
