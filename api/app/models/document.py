from sqlalchemy import Column, String, TIMESTAMP, SmallInteger, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
# import uuid

from app.models.base import Base
from app.core.utils import generate_uuid



class Document(Base):
    __tablename__ = "documents"

    id = Column(UUID(as_uuid=True), primary_key=True, default=generate_uuid())
    original_filename = Column(String, nullable=False)
    content_type = Column(String, nullable=False)
    storage_provider = Column(String, nullable=False)
    storage_bucket = Column(String, nullable=False)
    storage_key = Column(String, nullable=False)
    status_id = Column(
        SmallInteger,
        ForeignKey("document_statuses.id"),
        nullable=False,
    )
    created_at = Column(TIMESTAMP, server_default=func.now())

    status = relationship("DocumentStatus")

