from fastapi import FastAPI

from di.container import Container
from core.exceptions import TooManyRoomsException, InvalidRoomNameException, RoomNotExistException, \
    MemberNotExistException, UserNotAdminException
from presentation.fastapi.exception_handler import too_many_rooms_handler, invalid_room_name_handler, \
    room_not_exists_handler, member_not_exists_handler, user_not_admin_handler
from presentation.fastapi.routes.example import router as example_router
from presentation.fastapi.routes.room import router as room_router
from presentation.fastapi.routes.user import router as user_router


def create_api_app(container: Container) -> FastAPI:
    app = FastAPI(title="SaintBot API", docs_url="/docs")

    app.state.container = container

    app.add_exception_handler(TooManyRoomsException, too_many_rooms_handler)
    app.add_exception_handler(InvalidRoomNameException, invalid_room_name_handler)
    app.add_exception_handler(RoomNotExistException, room_not_exists_handler)
    app.add_exception_handler(MemberNotExistException, member_not_exists_handler)
    app.add_exception_handler(UserNotAdminException, user_not_admin_handler)

    app.include_router(example_router, prefix="/api", tags=["example"])
    app.include_router(room_router, prefix="/api/rooms", tags=["rooms"])
    app.include_router(user_router, prefix="/api/users", tags=["users"])
    return app
