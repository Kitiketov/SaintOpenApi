from fastapi import FastAPI

from di.container import Container
from core.exceptions import TooManyRoomsException, InvalidRoomNameException
from presentation.fastapi.exception_handler import too_many_rooms_handler, invalid_room_name_handler
from presentation.fastapi.routes.example import router as example_router
from presentation.fastapi.routes.room import router as room_router


def create_api_app() -> FastAPI:
    app = FastAPI(title="SaintBot API", docs_url="/docs")

    app.state.container = Container()

    app.add_exception_handler(TooManyRoomsException, too_many_rooms_handler)
    app.add_exception_handler(InvalidRoomNameException, invalid_room_name_handler)

    app.include_router(example_router, prefix="/api", tags=["example"])
    app.include_router(room_router, prefix="/api", tags=["rooms"])
    return app
