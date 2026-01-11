from strawberry.fastapi import GraphQLRouter
from graphql_api.context import get_context


from graphql_api.schema import schema

graphql_app = GraphQLRouter(
    schema,
    context_getter=get_context,
    graphiql=True,
)
