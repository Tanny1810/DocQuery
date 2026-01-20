import strawberry
from typing import Optional


@strawberry.type
class PageInfo:
    has_next_page: bool
    end_cursor: Optional[str]
