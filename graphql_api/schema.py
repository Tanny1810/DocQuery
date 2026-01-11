# graphql/schema.py
import strawberry
from typing import List

from graphql_api.types.document import DocumentType
from graphql_api.resolvers.documents import get_documents


@strawberry.type
class Query:
    documents: List[DocumentType] = strawberry.field(
        resolver=get_documents
    )


schema = strawberry.Schema(query=Query)
