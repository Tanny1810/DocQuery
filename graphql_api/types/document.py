# graphql/types/document.py
import strawberry
from datetime import datetime


@strawberry.type
class DocumentType:
    id: str
    filename: str
    status: str
    created_at: datetime
