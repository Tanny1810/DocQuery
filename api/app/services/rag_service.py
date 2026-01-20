from sqlalchemy.orm import Session

from app.models import User
from app.rag.strategies.registry import RAGStrategyRegistry

def query_documents(
    *,
    db: Session,
    query: str,
    top_k: int,
    user: User,
    rag_mode: str = "naive",
):
    strategy = RAGStrategyRegistry.get(rag_mode)
    return strategy.run(
        db=db,
        query=query,
        top_k=top_k,
        user=user,
    )