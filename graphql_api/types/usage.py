import strawberry


@strawberry.type
class UsageType:
    total_documents: int
    total_chunks: int
    total_queries: int
