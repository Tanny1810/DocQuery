import strawberry
from typing import Optional


@strawberry.type
class SourceType:
    document_id: str
    filename: str
    chunk_index: int
    page_number: Optional[int]
    section_title: Optional[str]
    score: float
