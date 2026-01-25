# graphql_api/resolvers/ask.py
from strawberry.types import Info
from strawberry.exceptions import GraphQLError

from api.app.services.rag_service import query_documents
from api.app.core.rate_limit import RateLimitExceeded
from graphql_api.types.rag import RAGResponse, Source
from graphql_api.types.rag_debug import RAGDebugMetadataType, RetrievedChunkDebugType


def query_documents_resolver(
    info: Info,
    query: str,
    top_k: int = 5,
):
    db = info.context.db
    user = info.context.user

    if user is None:
        raise GraphQLError("Authentication required")
    result = query_documents(
        db=db,
        query=query,
        top_k=top_k,
        user=user,
    )
    debug = result.get("debug")
    try:
        return RAGResponse(
            answer=result["answer"],
            confidence=result["confidence"],
            sources=[
                Source(
                    document_id=str(s["document_id"]),
                    chunk_index=s["chunk_index"],
                )
                for s in result["sources"]
            ],
            debug=(
                RAGDebugMetadataType(
                    retrieved_chunks=[
                        RetrievedChunkDebugType(**c) for c in debug["retrieved_chunks"]
                    ],
                    retrieved_count=debug["retrieved_count"],
                    used_in_prompt=debug["used_in_prompt"],
                    prompt_length=debug["prompt_length"],
                    fallback_used=debug["fallback_used"],
                )
                if debug
                else None
            ),
        )
    except RateLimitExceeded as e:
        # ✅ GraphQL-friendly error
        raise GraphQLError(str(e))
