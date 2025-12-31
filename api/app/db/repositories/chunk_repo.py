from sqlalchemy.orm import Session
from app.models.chunk import Chunk
from app.models.document import Document
from app.constants.document_status import DocumentStatus


def get_chunks_for_rag(
    db: Session,
    vector_ids: list[int],
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
            Document.status_id.in_(
                [DocumentStatus.READY, DocumentStatus.PARTIAL]
            ),
        )
        .all()
    )
