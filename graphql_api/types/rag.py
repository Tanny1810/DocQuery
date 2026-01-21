# graphql_api/types/rag.py
import strawberry
from typing import List


@strawberry.type
class Source:
    document_id: str
    chunk_index: int


@strawberry.type
class RAGResponse:
    answer: str
    sources: List[Source]
    confidence: float | None = None
