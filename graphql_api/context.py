from strawberry.fastapi.context import BaseContext
from fastapi import Request

from api.app.db.session import SessionLocal
from api.app.core.jwt_utils import get_user_from_token
from api.app.models import User


class GraphQLContext(BaseContext):
    def __init__(self, request: Request):
        self.db = SessionLocal()
        self.request = request

        auth_header = request.headers.get("Authorization")
        self.user: User | None = None

        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ", 1)[1]
            self.user = get_user_from_token(token, self.db)


def get_context(request: Request) -> GraphQLContext:
    return GraphQLContext(request)
