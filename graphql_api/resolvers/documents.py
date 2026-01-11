# graphql/resolvers/documents.py
from typing import List

from graphql_api.types.document import DocumentType


def get_documents() -> List[DocumentType]:
    """
    Temporary static resolver.
    Next step: connect DB.
    """
    return [
        DocumentType(
            id="1",
            filename="example.pdf",
            status="processed",
            created_at="2024-01-01T00:00:00",
        )
    ]
