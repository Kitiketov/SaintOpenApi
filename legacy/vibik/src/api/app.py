from fastapi import FastAPI

from src.api.routes.notify import router as notify_router


def create_api_app() -> FastAPI:
    app = FastAPI()
    app.include_router(notify_router, prefix="/api/moderation", tags=["moderation"])
    return app
