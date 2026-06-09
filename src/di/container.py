from punq import Container

from core.services.room_service import IRoomService, RoomService
from infrastructure.repositories.SaintRepository import SqliteSaintRepository
from infrastructure.repositories.interfaces.ISaintRepository import ISaintRepository
from config.settings import Settings
from presentation.fastapi.routes.example import IExampleRepository, ExampleRepository


def init_container(settings: Settings) -> Container:
    """Инициализация DI-контейнера"""
    container = Container()
    container.register(Settings, instance=settings)

    container.register(IExampleRepository, ExampleRepository)
    container.register(IRoomService, RoomService)

    container.register(ISaintRepository, SqliteSaintRepository)
    return container
