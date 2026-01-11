from sqlalchemy.orm import Session
from app.models.chunk import Chunk
from app.models.document import Document
from app.models import User
from shared.constants.document_status import DocumentStatus


def get_chunks_for_rag(
    db: Session,
    vector_ids: list[int],
    current_user: User,
):
    return (
        db.query(
            Chunk.document_id,
            Chunk.chunk_index,
            Chunk.content,
            Chunk.vector_id,
        )
        .join(Document, Document.id == Chunk.document_id)
        .filter(
            Chunk.vector_id.in_(vector_ids),
            Document.user_id == current_user.id,
            Document.status_id.in_([DocumentStatus.READY, DocumentStatus.PARTIAL]),
        )
        .all()
    )
