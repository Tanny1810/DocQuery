# graphql/schema.py
import strawberry
from typing import List

from graphql_api.types.document_connection import DocumentConnection
from graphql_api.types.document import DocumentType
from graphql_api.types.usage import UsageType
from graphql_api.types.rag import RAGResponse
from graphql_api.resolvers.documents_paginated import get_documents_paginated
from graphql_api.resolvers.documents import get_document_by_id
from graphql_api.resolvers.documents import get_documents
from graphql_api.resolvers.usage import get_usage
from graphql_api.resolvers.queries import query_documents_resolver


@strawberry.type
class Query:
    documents: List[DocumentType] = strawberry.field(resolver=get_documents)

    document_connection: DocumentConnection = strawberry.field(
        resolver=get_documents_paginated
    )

    document: DocumentType | None = strawberry.field(resolver=get_document_by_id)

    usage: UsageType = strawberry.field(resolver=get_usage)

    ask: RAGResponse  = strawberry.field(resolver=query_documents_resolver)


schema = strawberry.Schema(query=Query)
