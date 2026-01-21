from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.schemas.v1.auth import RegisterRequest, LoginRequest, TokenResponse
from app.models import User
from app.core.security import register_user, check_user
from app.db.session import get_db
from shared.config.logging import get_logger

logger = get_logger(__name__)

router = APIRouter()


@router.post("/register", status_code=201)
def register(data: RegisterRequest, db: Session = Depends(get_db)):
    register_user(data=data, db=db)
    return {"message": "User registered successfully"}


@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user_token = check_user(data=data, db=db)
    return {"access_token": user_token}
