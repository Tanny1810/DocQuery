from sqlalchemy import (
    Column,
    Text,
    TIMESTAMP,
    ForeignKey,
    String,
)
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func

from app.core.utils import generate_uuid
from app.models.base import Base


class QueryAudit(Base):
    __tablename__ = "query_audit"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=generate_uuid,
    )

    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    query_text = Column(Text, nullable=False)

    rag_mode = Column(String(32), nullable=False)

    document_ids = Column(
        JSONB,
        nullable=False,
        default=list,
    )

    created_at = Column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        nullable=False,
        index=True,
    )
