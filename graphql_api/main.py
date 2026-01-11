# graphql/main.py
import strawberry
from strawberry.fastapi import GraphQLRouter

from graphql_api.schema import schema

graphql_app = GraphQLRouter(
    schema,
)
