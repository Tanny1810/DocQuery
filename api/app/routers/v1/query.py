from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.rag_service import query_documents
from app.schemas.query import QueryRequest
from shared.config.logging import get_logger


logger = get_logger(__name__)

router = APIRouter()


@router.post("/search")
def query_docs(payload: QueryRequest, db: Session = Depends(get_db)):
    return query_documents(
        db=db,
        query=payload.query,
        top_k=payload.top_k,
    )
