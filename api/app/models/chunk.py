from sqlalchemy import Column, Integer, Text, ForeignKey, UniqueConstraint, Index
from sqlalchemy.dialects.postgresql import UUID, TSVECTOR

from app.models.base import Base


class Chunk(Base):
    __tablename__ = "chunks"

    id = Column(Integer, primary_key=True)
    document_id = Column(
        UUID(as_uuid=True),
        ForeignKey("documents.id", ondelete="CASCADE"),
        nullable=False,
    )
    chunk_index = Column(Integer, nullable=False)
    content = Column(Text, nullable=False)
    vector_id = Column(Integer, nullable=False)
    tsv = Column(TSVECTOR, nullable=False)
    page_number = Column(Integer, nullable=True)
    section_title = Column(Text, nullable=True)

    __table_args__ = (
        UniqueConstraint("document_id", "chunk_index"),
        Index("idx_chunks_tsv", "tsv", postgresql_using="gin"),
    )
