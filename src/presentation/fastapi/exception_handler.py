from fastapi import Request
from fastapi.responses import JSONResponse

from core.exceptions import (
    TooManyRoomsException,
    InvalidRoomNameException,
    RoomNotExistException,
    MemberNotExistException,
    UserNotAdminException,
    JoinTooLateException,
    UserAlreadyExistException,
)
from infrastructure.api_client.exceptions import APIError


async def base_exception_handler(request: Request, exc: APIError) -> JSONResponse:
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})


async def too_many_rooms_handler(request: Request, exc: TooManyRoomsException):
    return JSONResponse(status_code=400, content={"detail": "Too many rooms"})


async def invalid_room_name_handler(request: Request, exc: InvalidRoomNameException):
    return JSONResponse(status_code=422, content={"detail": "Invalid room name"})


async def room_not_exists_handler(request: Request, exc: RoomNotExistException):
    return JSONResponse(status_code=404, content={"detail": f"Room '{exc.room_name}' not exists"})


async def member_not_exists_handler(request: Request, exc: MemberNotExistException):
    return JSONResponse(status_code=403, content={"detail": f"Member not exists in room '{exc.room_name}'"})


async def user_not_admin_handler(request: Request, exc: UserNotAdminException):
    return JSONResponse(status_code=403, content={"detail": f"User is not admin of room '{exc.room_name}'"})


async def join_too_late_handler(request: Request, exc: JoinTooLateException):
    return JSONResponse(status_code=422, content={"detail": "Event started"})


async def user_already_exists_handler(request: Request, exc: UserAlreadyExistException):
    return JSONResponse(status_code=403, content={"detail": f"User '{exc.room_name}' already exists"})
