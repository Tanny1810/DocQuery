# FastAPI main application

from fastapi import FastAPI

from app.core.config import settings
from api.app.routers.router import router_v1

from shared.config.logging import configure_logging
from api.app.core.middleware import RequestIdMiddleware
from graphql_api.main import graphql_app


def create_app() -> FastAPI:
    # configure global logging early
    configure_logging(settings.LOG_LEVEL)

    app = FastAPI(title=settings.APP_NAME, debug=settings.DEBUG)

    # register middleware that sets X-Request-Id and logs
    app.add_middleware(RequestIdMiddleware)

    app.include_router(router_v1)
    app.include_router(graphql_app, prefix="/graphql")

    return app


app = create_app()
