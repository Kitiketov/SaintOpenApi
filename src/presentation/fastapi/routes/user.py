from fastapi import APIRouter, Depends

from core.schemas.user import User
from core.services.user_service import IUserService
from presentation.fastapi.auth import get_current_user
from presentation.fastapi.dependencies import get_service
from presentation.fastapi.schemas.user import GetRoomsResponse

router = APIRouter()


@router.get("/me/rooms")
async def get_rooms(
    as_admin: bool | None = None,
    current_user: User = Depends(get_current_user),
    user_service: IUserService = Depends(get_service(IUserService)),
) -> GetRoomsResponse:
    rooms = await user_service.get_rooms(current_user.id, as_admin)
    return GetRoomsResponse(rooms=rooms)
