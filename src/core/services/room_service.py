from abc import ABC, abstractmethod

from core.exceptions import TooManyRoomsException, InvalidRoomNameException
from core.schemas.user import User
from infrastructure.repositories.interfaces.ISaintRepository import ISaintRepository


class IRoomService(ABC):
    @abstractmethod
    async def prepare_create_room(self, user: User) -> None:
        pass

    @abstractmethod
    async def create_new_room(self, room_name: str, user_id: int) -> str:
        pass


class RoomService(IRoomService):
    def __init__(self, repo: ISaintRepository):
        self.repo = repo

    async def prepare_create_room(self, user: User) -> None:
        room_count = await self.repo.count_user_room(user.id)

        if room_count > 5:
            raise TooManyRoomsException()

        await self.repo.add_user(user)

    async def create_new_room(self, room_name: str, user_id: int) -> str:
        room_id = await self.repo.create_room(room_name, user_id)

        if not room_id:
            raise InvalidRoomNameException()

        return room_id
