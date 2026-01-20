from typing import Optional
from strawberry.types import Info
from sqlalchemy import and_, or_, desc

from api.app.models import Document
from graphql_api.types.document_connection import (
    DocumentConnection,
    DocumentEdge,
)
from graphql_api.types.document import DocumentType
from graphql_api.types.pagination import PageInfo
from graphql_api.utils.cursor import encode_cursor, decode_cursor


def get_documents_paginated(
    info: Info,
    first: int = 10,
    after: Optional[str] = None,
) -> DocumentConnection:
    db = info.context.db
    user = info.context.user

    if user is None:
        return DocumentConnection(
            edges=[],
            page_info=PageInfo(has_next_page=False, end_cursor=None),
        )

    query = (
        db.query(Document)
        .filter(Document.user_id == user.id)
        .order_by(desc(Document.created_at), desc(Document.id))
    )

    # Apply cursor if present
    if after:
        created_at, doc_id = decode_cursor(after)
        query = query.filter(
            or_(
                Document.created_at < created_at,
                and_(
                    Document.created_at == created_at,
                    Document.id < doc_id,
                ),
            )
        )

    # Fetch one extra row to check hasNextPage
    rows = query.limit(first + 1).all()

    has_next_page = len(rows) > first
    rows = rows[:first]

    edges = []
    for doc in rows:
        cursor = encode_cursor(doc.created_at, str(doc.id))
        edges.append(
            DocumentEdge(
                node=DocumentType(
                    id=str(doc.id),
                    filename=doc.original_filename,
                    content_type=doc.content_type,
                    storage_provider=doc.storage_provider,
                    status=doc.status.name,
                    created_at=doc.created_at,
                ),
                cursor=cursor,
            )
        )

    end_cursor = edges[-1].cursor if edges else None

    return DocumentConnection(
        edges=edges,
        page_info=PageInfo(
            has_next_page=has_next_page,
            end_cursor=end_cursor,
        ),
    )
