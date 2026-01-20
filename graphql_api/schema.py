# graphql/schema.py
import strawberry
from typing import List

from graphql_api.types.document import DocumentType
from graphql_api.resolvers.documents import get_documents
from graphql_api.resolvers.documents import get_document_by_id
from graphql_api.resolvers.documents_paginated import get_documents_paginated
from graphql_api.types.document_connection import DocumentConnection


@strawberry.type
class Query:
    documents: List[DocumentType] = strawberry.field(
        resolver=get_documents
    ) 

    document_connection: DocumentConnection = strawberry.field(
        resolver=get_documents_paginated
    )

    document: DocumentType | None = strawberry.field(
        resolver=get_document_by_id
    )


schema = strawberry.Schema(query=Query)
