# graphql_api/types/rag.py
import strawberry
from typing import List

from graphql_api.types.rag_debug import RAGDebugMetadataType


@strawberry.type
class Source:
    document_id: str
    chunk_index: int


@strawberry.type
class RAGResponse:
    answer: str
    sources: List[Source]
    confidence: float | None = None
    debug: RAGDebugMetadataType | None
