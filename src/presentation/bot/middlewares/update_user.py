from aiogram import BaseMiddleware

from infrastructure.repositories.interfaces.ISaintRepository import ISaintRepository


class UpdateUserMiddleware(BaseMiddleware):
    def __init__(self, repo: ISaintRepository):
        self.repo = repo

    async def __call__(self, handler, event, data):
        user = getattr(event, "from_user", None)
        if user:
            await self.repo.update_user(user)
        return await handler(event, data)
