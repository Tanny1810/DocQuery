from typing import List
from strawberry.types import Info
from sqlalchemy import func

from shared.constants.document_status import DocumentStatus
from app.models.query_audit import QueryAudit
from api.app.models import Document, Chunk
from graphql_api.types.usage import UsageType


def get_usage(info: Info) -> UsageType:
    """
    Fetch documents from Relational DB.
    """
    db = info.context.db
    user = info.context.user

    if user is None:
        return UsageType(
            total_documents=0,
            total_chunks=0,
            total_queries=0,
            total_storage_used_mb=0.0,
        )

    # 1️⃣ Total documents
    total_documents = (
        db.query(func.count(Document.id))
        .filter(Document.user_id == user.id)
        .scalar()
        or 0
    )

    # 2️⃣ Total chunks (READY / PARTIAL docs only)
    total_chunks = (
        db.query(func.count(Chunk.id))
        .join(Document, Document.id == Chunk.document_id)
        .filter(
            Document.user_id == user.id,
            Document.status_id.in_(
                [DocumentStatus.READY, DocumentStatus.PARTIAL]
            ),
        )
        .scalar()
        or 0
    )

    # 3️⃣ Total queries (REAL now 🎉)
    total_queries = (
        db.query(func.count(QueryAudit.id))
        .filter(QueryAudit.user_id == user.id)
        .scalar()
        or 0
    )

    return UsageType(
        total_documents=total_documents,
        total_chunks=total_chunks,
        total_queries=total_queries,
    )
