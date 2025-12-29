from sqlalchemy import Column, SmallInteger, String, Text
from app.models.base import Base


class DocumentStatus(Base):
    __tablename__ = "document_statuses"

    id = Column(
        SmallInteger,
        primary_key=True,
        autoincrement=False,  # IMPORTANT
    )

    name = Column(
        String,
        nullable=False,
        unique=True,
    )

    description = Column(
        Text,
        nullable=True,
    )