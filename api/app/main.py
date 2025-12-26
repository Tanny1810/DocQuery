# FastAPI main application

from fastapi import FastAPI
from api.app.core.config import settings
from api.app.routers.router import router_v1

from shared.config.logging import configure_logging
from api.app.core.middleware import RequestIdMiddleware


def create_app() -> FastAPI:
    # configure global logging early
    configure_logging(settings.LOG_LEVEL)

    app = FastAPI(
        title=settings.APP_NAME,
        debug=settings.DEBUG
    )

    # register middleware that sets X-Request-Id and logs
    app.add_middleware(RequestIdMiddleware)

    app.include_router(router_v1)

    return app


app = create_app()
