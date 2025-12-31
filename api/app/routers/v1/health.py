from fastapi import APIRouter
from api.app.schemas.health import HealthResponse

router = APIRouter()


@router.get(path="", response_model=HealthResponse)
async def health_check():
    return HealthResponse(status="healthy")
