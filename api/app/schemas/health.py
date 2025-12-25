from pydantic import BaseModel
from typing import Literal
from api.app.core.config import settings


class HealthResponse(BaseModel):
    status: Literal["healthy", "unhealthy"]
    service: str =settings.APP_NAME
