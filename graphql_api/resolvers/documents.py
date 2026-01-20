from typing import List
from strawberry.types import Info
from sqlalchemy.orm import joinedload

from graphql_api.types.document import DocumentType
from api.app.models import Document


def get_documents(info: Info) -> List[DocumentType]:
    """
    Fetch documents from Relational DB.
    """
    db = info.context.db
    user = info.context.user

    if user is None:
        return []

    documents = (
        db.query(Document)
        .options(joinedload(Document.status))
        .filter(Document.user_id == user.id)
        .all()
    )

    return [
        DocumentType(
            id=str(doc.id),
            filename=doc.original_filename,
            content_type=doc.content_type,
            storage_provider=doc.storage_provider,
            status=doc.status.name,
            created_at=doc.created_at,
        )
        for doc in documents
    ]


def get_document_by_id(info: Info, document_id: str) -> DocumentType | None:
    """
    Fetch document by ID from Relational DB.
    """
    db = info.context.db
    user = info.context.user

    if user is None:
        return None

    document = (
        db.query(Document)
        .options(joinedload(Document.status))
        .filter(Document.user_id == user.id, Document.id == document_id)
        .first()
    )

    if not document:
        return None

    return DocumentType(
        id=str(document.id),
        filename=document.original_filename,
        content_type=document.content_type,
        storage_provider=document.storage_provider,
        status=document.status.name,
        created_at=document.created_at,
    )
