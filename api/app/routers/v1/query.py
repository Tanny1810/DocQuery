from fastapi import APIRouter, Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session

from api.app.core.rate_limit import RateLimitExceeded
from app.models import User
from app.schemas.v1.query import QueryRequest
from app.services.rag_service import query_documents
from app.core.security import get_current_user
from app.db.session import get_db
from shared.config.logging import get_logger


logger = get_logger(__name__)

router = APIRouter()


@router.post("/search")
def query_docs(
    payload: QueryRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        return query_documents(
            db=db,
            query=payload.query,
            top_k=payload.top_k,
            user=current_user,
            rag_mode=payload.rag_mode,
        )
    except RateLimitExceeded as e:
        raise HTTPException(
            status_code=429,
            detail=str(e),
        )
