# graphql_api/resolvers/ask.py
from strawberry.types import Info
from strawberry.exceptions import GraphQLError

from api.app.services.rag_service import query_documents
from api.app.core.rate_limit import RateLimitExceeded
from graphql_api.types.rag import RAGResponse, Source


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
            confidence=result.get("confidence"),
        )
    except RateLimitExceeded as e:
        # ✅ GraphQL-friendly error
        raise GraphQLError(str(e))
