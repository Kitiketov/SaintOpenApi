import asyncio
from abc import ABC, abstractmethod

from infrastructure.repositories.interfaces.ISaintRepository import ISaintRepository


class IUserService(ABC):
    @abstractmethod
    async def get_rooms(self, user_id: int, as_admin: bool):
        pass


class UserService(IUserService):
    def __init__(self, repo: ISaintRepository):
        self.repo = repo

    async def get_rooms(self, user_id: int, as_admin: bool | None) -> dict[str, list[str]]:
        if as_admin is None:
            admin_rooms, member_rooms = await asyncio.gather(
                self.repo.get_my_rooms(user_id, as_admin=True),
                self.repo.get_my_rooms(user_id, as_admin=False)
            )

            return {
                "admin": admin_rooms,
                "member": member_rooms,
            }

        rooms = await self.repo.get_my_rooms(user_id, as_admin)

        return {
            "admin": rooms if as_admin else [],
            "member": rooms if not as_admin else [],
        }
