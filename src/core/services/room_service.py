from abc import ABC, abstractmethod

from core.exceptions import TooManyRoomsException, InvalidRoomNameException, RoomNotExistException, \
    UserNotAdminException, MemberNotExistException
from core.schemas.user import User
from infrastructure.repositories.interfaces.ISaintRepository import ISaintRepository


class IRoomService(ABC):
    @abstractmethod
    async def prepare_create_room(self, user: User) -> None:
        pass

    @abstractmethod
    async def create_new_room(self, room_name: str, user_id: int) -> str:
        pass

    @abstractmethod
    async def get_room_name(self, room_iden: str) -> str:
        pass

    @abstractmethod
    async def get_room_settings(self, room_iden: str, user_id: int, require_admin: bool) -> tuple[str | bool, str | None, str | None, str | None]:
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

    async def get_room_name(self, room_iden: str) -> str:
        return f"{room_iden[:-4]}:{room_iden[-4:]}"

    async def get_room_settings(self, room_iden: str, user_id: int, require_admin: bool) -> tuple[str | bool, str | None, str | None, str | None]:
        status = await self.repo.check_room_and_member(user_id, room_iden)
        room_name = await self.get_room_name(room_iden)

        if status == "ROOM NOT EXISTS":
            raise RoomNotExistException(room_name)

        if require_admin:
            admin_id = await self.repo.get_room_admin(room_iden)
            if admin_id != user_id:
                raise UserNotAdminException(room_name)
        else:
            if status == "MEMBER NOT EXISTS":
                raise MemberNotExistException(room_name)

        _, price, event_time, exchange_type = await self.repo.get_room_settings(room_iden)
        return room_name, price, event_time, exchange_type


