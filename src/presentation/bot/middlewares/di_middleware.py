from aiogram import BaseMiddleware
from punq import Container

from infrastructure.api_client.room_client import RoomClient


class DiMiddleware(BaseMiddleware):
    def __init__(self, container: Container):
        self.container = container

    # todo: добавить остальные клиенты (если будет много, то это наверное не оч подход)
    async def __call__(self, handler, event, data):
        data["room_client"] = self.container.resolve(RoomClient)
        return await handler(event, data)
