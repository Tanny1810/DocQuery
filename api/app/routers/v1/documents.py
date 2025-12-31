from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from shared.config.logging import get_logger
from app.services.document_service import upload_document

logger = get_logger(__name__)

router = APIRouter()


@router.post(path="/upload")
async def upload_doc(file: UploadFile = File(...), db: Session = Depends(get_db)):
    return await upload_document(file=file, db=db)
