import httpx
from authx import AuthX
from punq import Container

from config.auth import init_authx
from core.services.room_service import IRoomService, RoomService
from core.services.user_service import UserService, IUserService
from infrastructure.api_client.room_client import RoomClient
from infrastructure.repositories.SaintRepository import SqliteSaintRepository
from infrastructure.repositories.interfaces.ISaintRepository import ISaintRepository
from config.settings import Settings
from presentation.fastapi.routes.example import IExampleRepository, ExampleRepository


def init_container(settings: Settings) -> Container:
    """Инициализация DI-контейнера"""
    container = Container()
    container.register(Settings, instance=settings)
    security = init_authx(settings)
    container.register(AuthX, instance=security)
    container.register(httpx.AsyncClient, instance=httpx.AsyncClient(base_url=settings.base_api_url))

    container.register(RoomClient, RoomClient)

    container.register(IExampleRepository, ExampleRepository)
    container.register(IRoomService, RoomService)
    container.register(IUserService, UserService)
    container.register(ISaintRepository, SqliteSaintRepository)

    return container
