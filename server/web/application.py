from fastapi import FastAPI
from fastapi.responses import UJSONResponse
from server.web.api.router import api_router


def get_app() -> FastAPI:
    """
    Get FastAPI application.

    This is the main constructor of an application.

    :return: application.
    """
    app = FastAPI(
        title="Server IsAGame",
        description="",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        default_response_class=UJSONResponse,
    )
    app.include_router(router=api_router, prefix="/api")
    return app
