import httpx
from punq import Container

from core.services.room_service import IRoomService, RoomService
from infrastructure.api_client.room_client import RoomClient
from infrastructure.repositories.SaintRepository import SqliteSaintRepository
from infrastructure.repositories.interfaces.ISaintRepository import ISaintRepository
from config.settings import Settings
from presentation.fastapi.routes.example import IExampleRepository, ExampleRepository


def init_container(settings: Settings) -> Container:
    """Инициализация DI-контейнера"""
    container = Container()
    container.register(Settings, instance=settings)

    container.register(httpx.AsyncClient, instance=httpx.AsyncClient(base_url=settings.base_api_url))

    container.register(RoomClient, RoomClient)

    container.register(IExampleRepository, ExampleRepository)
    container.register(IRoomService, RoomService)
    container.register(ISaintRepository, SqliteSaintRepository)

    return container
