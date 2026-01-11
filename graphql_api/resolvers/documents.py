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
    documents = db.query(Document).options(joinedload(Document.status)).all()

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
