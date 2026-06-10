from abc import ABC, abstractmethod

from infrastructure.repositories.interfaces.ISaintRepository import ISaintRepository


class IUserService(ABC):
    @abstractmethod
    async def get_rooms(self, user_id: int, as_admin: bool):
        pass


class UserService(IUserService):
    def __init__(self, repo: ISaintRepository):
        self.repo = repo

    async def get_rooms(self, user_id: int, as_admin: bool):
        rooms = await self.repo.get_my_rooms(user_id, as_admin)
        return rooms
