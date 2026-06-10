from fastapi import APIRouter, Depends

from core.services.user_service import IUserService
from presentation.fastapi.dependencies import get_service
from presentation.fastapi.schemas.user import GetRoomsResponse

router = APIRouter()


@router.get("/{user_id}/rooms")
async def get_rooms(
    user_id: int, as_admin: bool, user_service: IUserService = Depends(get_service(IUserService))
) -> GetRoomsResponse:
    rooms = await user_service.get_rooms(user_id, as_admin)
    return GetRoomsResponse(rooms=rooms)
