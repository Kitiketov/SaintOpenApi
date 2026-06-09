from fastapi import FastAPI

from src.presentation.fastapi.routes.example import router as example_router


def create_api_app() -> FastAPI:
    app = FastAPI(title="SaintBot API", docs_url="/docs")
    app.include_router(example_router, prefix="/api", tags=["example"])
    return app
