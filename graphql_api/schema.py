# graphql/schema.py
import strawberry
from typing import List

from graphql_api.types.document import DocumentType
from graphql_api.resolvers.documents import get_documents
from graphql_api.resolvers.documents import get_document_by_id


@strawberry.type
class Query:
    documents: List[DocumentType] = strawberry.field(
        resolver=get_documents
    )

    document: DocumentType | None = strawberry.field(
        resolver=get_document_by_id
    )


schema = strawberry.Schema(query=Query)
