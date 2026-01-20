from pydantic import BaseModel


class QueryRequest(BaseModel):
    query: str
    top_k: int = 5
    rag_mode: str = "naive"
