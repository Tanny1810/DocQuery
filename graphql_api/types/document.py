# graphql/types/document.py
import strawberry
from datetime import datetime


@strawberry.type
class DocumentType:
    id: str
    filename: str
    content_type: str
    storage_provider: str
    status: str
    created_at: datetime
