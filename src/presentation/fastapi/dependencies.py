from fastapi import Request

from punq import Container


def get_service[T](service_type: T):
    """
    Адаптер для FastAPI Depends.
    Принимает абстракцию и возвращает её реализацию из контейнера.
    """

    def _resolve(request: Request) -> T:
        container: Container = request.app.state.container
        return container.resolve(service_type)

    return _resolve
