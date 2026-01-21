import strawberry
from graphql_api.resolvers.queries import query_documents_resolver as ask
from graphql_api.types.rag import RAGResponse


@strawberry.type
class QueryType:
    ask: RAGResponse = strawberry.field(resolver=ask)
