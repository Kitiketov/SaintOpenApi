from fastapi import Request
from fastapi.responses import JSONResponse

from core.exceptions import TooManyRoomsException, InvalidRoomNameException


async def too_many_rooms_handler(request: Request, exc: TooManyRoomsException):
    return JSONResponse(status_code=400, content={"detail": "Too many rooms"})


async def invalid_room_name_handler(request: Request, exc: InvalidRoomNameException):
    return JSONResponse(status_code=422, content={"detail": "Invalid room name"})
