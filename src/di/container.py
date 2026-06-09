from punq import Container

from presentation.fastapi.routes.room import IRoomRepository, RoomRepository
from src.infrastructure.repositories.SaintRepository import SqliteSaintRepository
from src.infrastructure.repositories.interfaces.ISaintRepository import ISaintRepository
from src.config.settings import Settings
from src.presentation.fastapi.routes.example import IExampleRepository, ExampleRepository


def init_container(settings: Settings) -> Container:
    """Инициализация DI-контейнера"""
    container = Container()
    container.register(Settings, instance=settings)

    container.register(IExampleRepository, ExampleRepository)
    container.register(IRoomRepository, RoomRepository)

    container.register(ISaintRepository, SqliteSaintRepository)
    return container
