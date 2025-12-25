# FastAPI main application

from fastapi import FastAPI
from api.app.core.config import settings
from api.app.routers.router import router_v1


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.APP_NAME,
        debug=settings.DEBUG
    )

    app.include_router(router_v1)

    return app


app = create_app()
