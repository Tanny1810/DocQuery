import strawberry
from typing import List

from graphql_api.types.document import DocumentType
from graphql_api.types.pagination import PageInfo


@strawberry.type
class DocumentEdge:
    node: DocumentType
    cursor: str


@strawberry.type
class DocumentConnection:
    edges: List[DocumentEdge]
    page_info: PageInfo
