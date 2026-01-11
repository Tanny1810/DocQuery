from fastapi import APIRouter
from app.routers.v1.health import router as health_router
from app.routers.v1.documents import router as documents_router
from app.routers.v1.query import router as query_router
from app.routers.v1.auth import router as auth_router

router_v1 = APIRouter(prefix="/api/v1")
router_v1.include_router(health_router, prefix="/health", tags=["Health"])
router_v1.include_router(auth_router, prefix="/auth", tags=["Auth"])
router_v1.include_router(documents_router, prefix="/document", tags=["Document"])
router_v1.include_router(query_router, prefix="/query", tags=["Query"])
