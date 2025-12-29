from sqlalchemy.orm import Session
from app.models import Document
from app.constants.document_status import DocumentStatus

def create_document(
    db: Session,
    *,
    original_filename: str,
    content_type: str,
    storage_provider: str,
    storage_bucket: str,
    storage_key: str,
    status_id: int,
) -> Document:
    document = Document(
        original_filename=original_filename,
        content_type=content_type,
        storage_provider=storage_provider,
        storage_bucket=storage_bucket,
        storage_key=storage_key,
        status_id=status_id,
    )

    db.add(document)
    db.flush()
    db.refresh(document)
    return document

def update_document_status(
    db: Session,
    *,
    document_id,
    status_id: int,
):
    db.query(Document).filter(
        Document.id == document_id
    ).update({"status_id": status_id})
    db.flush()
