# graphql_api/types/rag.py
import strawberry
from typing import List

from graphql_api.types.rag_debug import RAGDebugMetadataType
from graphql_api.types.source import SourceType


@strawberry.type
class RAGResponse:
    answer: str
    sources: List[SourceType]
    confidence: float | None = None
    debug: RAGDebugMetadataType | None
