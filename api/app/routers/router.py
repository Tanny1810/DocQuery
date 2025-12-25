from fastapi import APIRouter
from api.app.routers.v1.health import router as health_router
from api.app.routers.v1.documents import router as documents_router

router_v1 = APIRouter(prefix="/api/v1")
router_v1.include_router(health_router, prefix="/health", tags=["Health"])
router_v1.include_router(documents_router, prefix="/document", tags=["Document"])
