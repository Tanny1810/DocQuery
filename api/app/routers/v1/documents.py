from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session

from app.models import User
from app.db.session import get_db
from app.core.security import get_current_user
from app.services.document_service import upload_document
from shared.config.logging import get_logger

logger = get_logger(__name__)

router = APIRouter()


@router.post(path="/upload")
async def upload_doc(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await upload_document(file=file, db=db, current_user=current_user)
