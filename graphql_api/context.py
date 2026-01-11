from strawberry.fastapi.context import BaseContext
from api.app.db.session import SessionLocal


class GraphQLContext(BaseContext):
    def __init__(self):
        self.db = SessionLocal()


def get_context():
    return GraphQLContext()
