import strawberry
from typing import List
from graphql_api.types.source import SourceType


@strawberry.type
class RAGDebugMetadataType:
    retrieved_chunks: List[SourceType]
    retrieved_count: int
    used_in_prompt: int
    prompt_length: int
    fallback_used: bool
