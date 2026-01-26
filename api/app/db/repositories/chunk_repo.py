from sqlalchemy.orm import Session
from sqlalchemy import text, func

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
            Chunk.page_number,
            Chunk.section_title,
            Document.original_filename.label("filename"),
        )
        .join(Document, Document.id == Chunk.document_id)
        .filter(
            Chunk.vector_id.in_(vector_ids),
            Document.user_id == current_user.id,
            Document.status_id.in_([DocumentStatus.READY, DocumentStatus.PARTIAL]),
        )
        .all()
    )


def search_chunks_bm25(
    *,
    db: Session,
    query: str,
    limit: int,
    current_user,
):
    """
    Keyword-based (BM25-style) chunk search using Postgres full-text search.
    """
    ts_query = text(
        """
        plainto_tsquery('english', :query)
        """
    )

    return (
        db.query(
            Chunk.document_id,
            Chunk.chunk_index,
            Chunk.content,
            Chunk.id.label("vector_id"),
            Chunk.page_number,
            Chunk.section_title,
            Document.original_filename.label("filename")
        )
        .join(Document, Document.id == Chunk.document_id)
        .filter(
            Document.user_id == current_user.id,
            Document.status_id.in_([DocumentStatus.READY, DocumentStatus.PARTIAL]),
            Chunk.tsv.op("@@")(ts_query),
        )
        .order_by(
            func.ts_rank(Chunk.tsv, func.plainto_tsquery("english", query)).desc()
        )
        .params(query=query)
        .limit(limit)
        .all()
    )
