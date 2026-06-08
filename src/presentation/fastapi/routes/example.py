from abc import ABC, abstractmethod

from fastapi import APIRouter, Request, Depends

from presentation.fastapi.dependencies import get_service
from presentation.fastapi.schemas.example import ExampleRequest, ExampleResponse


class IExampleRepository(ABC):
    @abstractmethod
    async def get_user(self, user_id: int) -> bool:
        pass


class ExampleRepository(IExampleRepository):

    async def get_user(self, user_id: int) -> bool:
        return True


router = APIRouter()


@router.post("/example")
async def example(payload: ExampleRequest, request: Request,
                  example_repo: IExampleRepository = Depends(get_service(IExampleRepository))) -> ExampleResponse:
    """
        EXXXAAAAMMMPPPLEEE
    """
    status = await example_repo.get_user(payload.id)

    return ExampleResponse(status=status)
