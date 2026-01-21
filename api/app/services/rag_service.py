from sqlalchemy.orm import Session

from app.models import User
from app.rag.strategies.registry import RAGStrategyRegistry
from api.app.db.repositories.query_audit_repo import create_query_audit
from api.app.core.rate_limit import check_rate_limit, RateLimitExceeded


def query_documents(
    *,
    db: Session,
    query: str,
    top_k: int,
    user: User,
    rag_mode: str = "naive",
):
    # 1️⃣ Rate limit check (BEFORE RAG)
    check_rate_limit(
        db=db,
        user_id=user.id,
    )

    # 2️⃣ Execute RAG
    strategy = RAGStrategyRegistry.get(rag_mode)
    result = strategy.run(
        db=db,
        query=query,
        top_k=top_k,
        user=user,
    )

    # 3️⃣ Write audit ONLY if RAG executed
    # (Even if answer is "I don't know", it is a valid query)
    create_query_audit(
        db=db,
        user_id=user.id,
        query_text=query,
        rag_mode=rag_mode,
        document_ids=[str(src["document_id"]) for src in result.get("sources", [])],
    )

    return result
