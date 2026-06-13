from aiogram import BaseMiddleware
from punq import Container

from infrastructure.api_client.room_client import RoomClient
from infrastructure.api_client.user_client import UserClient


class DiMiddleware(BaseMiddleware):
    def __init__(self, container: Container):
        self.container = container

    # todo: добавить остальные клиенты (если будет много, то это наверное не оч подход)
    async def __call__(self, handler, event, data):
        data.setdefault("room_client", self.container.resolve(RoomClient))
        data.setdefault("user_client", self.container.resolve(UserClient))

        return await handler(event, data)
