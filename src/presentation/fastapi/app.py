from fastapi import FastAPI

from di.container import Container
from core.exceptions import TooManyRoomsException, InvalidRoomNameException
from presentation.fastapi.exception_handler import too_many_rooms_handler, invalid_room_name_handler
from presentation.fastapi.routes.example import router as example_router
from presentation.fastapi.routes.room import router as room_router
from presentation.fastapi.routes.auth import router as auth_router
from presentation.fastapi.routes.index import router as index_router
from fastapi.templating import Jinja2Templates

def create_api_app(container: Container) -> FastAPI:
    app = FastAPI(title="SaintBot API", docs_url="/docs")

    templates = Jinja2Templates(directory="templates")
    app.state.container = container
    app.state.templates = templates

    app.add_exception_handler(TooManyRoomsException, too_many_rooms_handler)
    app.add_exception_handler(InvalidRoomNameException, invalid_room_name_handler)

    app.include_router(example_router, prefix="/api", tags=["example"])
    app.include_router(room_router, prefix="/api/rooms", tags=["rooms"])
    app.include_router(auth_router, prefix="/api/auth", tags=["auth"])
    app.include_router(index_router, prefix="", tags=["index"])
    return app
