from abc import ABC, abstractmethod
from typing import Any

from core.exceptions import (
    TooManyRoomsException,
    InvalidRoomNameException,
    RoomNotExistException,
    UserNotAdminException,
    MemberNotExistException,
    UserAlreadyExistException,
    JoinTooLateException,
)
from core.schemas.user import User
from infrastructure.repositories.interfaces.ISaintRepository import ISaintRepository
from presentation.fastapi.schemas.room import ConnectResponse


class IRoomService(ABC):
    @abstractmethod
    async def validate_room_creation(self, user: User) -> None:
        pass

    @abstractmethod
    async def create_new_room(self, room_name: str, user_id: int) -> str:
        pass

    @abstractmethod
    async def get_room_settings(
        self, room_iden: str, user_id: int, require_admin: bool
    ) -> tuple[str | bool, str | None, str | None, str | None]:
        pass

    async def connect_room(self, room_ident: str, user_id) -> bool:
        pass

    @abstractmethod
    async def get_members(self, room_iden: str, user_id: int) -> tuple[list, Any]:
        pass


class RoomService(IRoomService):
    def __init__(self, repo: ISaintRepository):
        self.repo = repo

    async def validate_room_creation(self, user: User) -> None:
        room_count = await self.repo.count_user_room(user.id)

        if room_count > 5:
            raise TooManyRoomsException()

        # todo: вынести эту логику в логин?
        await self.repo.add_user(user)

    async def create_new_room(self, room_name: str, user_id: int) -> str:
        room_id = await self.repo.create_room(room_name, user_id)

        if not room_id:
            raise InvalidRoomNameException()

        return room_id

    async def get_room_settings(
        self, room_iden: str, user_id: int, require_admin: bool
    ) -> tuple[str | bool, str | None, str | None, str | None]:
        status = await self.repo.check_room_and_member(user_id, room_iden)

        if status == "ROOM NOT EXISTS":
            raise RoomNotExistException(room_iden)
        elif require_admin:
            admin_id = await self.repo.get_room_admin(room_iden)
            if admin_id != user_id:
                raise UserNotAdminException(room_iden)
        elif status == "MEMBER NOT EXISTS":
            raise MemberNotExistException(room_iden)

        _, price, event_time, exchange_type = await self.repo.get_room_settings(room_iden)
        return room_iden, price, event_time, exchange_type

    async def connect_room(self, room_iden: str, user_id) -> bool:
        room_status = await self.repo.connect_to_room(room_iden, user_id)
        if room_status == "room_error":
            raise RoomNotExistException(room_iden)
        elif room_status == "user_error":
            raise UserAlreadyExistException
        elif room_status == "joined late":
            raise JoinTooLateException
        return True

    async def get_members(self, room_iden: str, user_id: int) -> tuple[list, Any]:
        is_member_or_admin = await self.repo.check_room_and_member(user_id, room_iden)

        if is_member_or_admin == "MEMBER NOT EXISTS":
            raise MemberNotExistException(room_iden)
        elif is_member_or_admin == "ROOM NOT EXISTS":
            raise RoomNotExistException(room_iden)

        member_list, admin, is_admin_member = await self.repo.get_members_list(room_iden)

        member_list = [User.from_row(m) for m in member_list]
        admin = User.from_row(admin)

        if is_admin_member:
            member_list.append(admin)

        return member_list, admin
