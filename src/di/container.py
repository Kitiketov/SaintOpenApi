from punq import Container
from src.config.settings import Settings
from src.presentation.fastapi.routes.example import IExampleRepository, ExampleRepository


def init_container(settings: Settings) -> Container:
    container = Container()
    container.register(Settings, instance=settings)
    container.register(IExampleRepository, ExampleRepository)
    return container