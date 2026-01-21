from sqlalchemy.orm import Session
from typing import Iterable

from app.models.query_audit import QueryAudit


def create_query_audit(
    *,
    db: Session,
    user_id,
    query_text: str,
    rag_mode: str,
    document_ids: Iterable[str],
):
    audit = QueryAudit(
        user_id=user_id,
        query_text=query_text,
        rag_mode=rag_mode,
        document_ids=list(document_ids),
    )

    db.add(audit)
    db.commit()

def count_queries_since(db: Session, user_id: str, since) -> int:
    return (
        db.query(QueryAudit)
        .filter(
            QueryAudit.user_id == user_id,
            QueryAudit.created_at >= since,
        )
        .count()
    )