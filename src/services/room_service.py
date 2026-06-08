from services.schemas.user import User
from src.infrastructure.db import db


class TooManyRoomsException(Exception): pass
class InvalidRoomNameException(Exception): pass


async def prepare_create_room(user: User) -> None:
    room_count = await db.count_user_room(user.id)

    if room_count > 5:
        raise TooManyRoomsException()

    await db.add_user(user)


async def create_new_room(room_name: str, user_id: int) -> None:
    room_id = await db.create_room(room_name, user_id)

    if not room_id:
        raise InvalidRoomNameException()

    return room_id
