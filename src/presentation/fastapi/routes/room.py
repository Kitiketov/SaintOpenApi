from fastapi import APIRouter, Depends

from core.schemas.user import User
from core.services.room_service import IRoomService
from presentation.fastapi.auth import get_current_user
from presentation.fastapi.dependencies import get_service
from presentation.fastapi.schemas.room import CreatePayload, PrepareResponse, CreateResponse

router = APIRouter()


@router.post("/prepare")
async def api_prepare_room(
    current_user: User = Depends(get_current_user),
    room_service: IRoomService = Depends(get_service(IRoomService))
) -> PrepareResponse:
    await room_service.prepare_create_room(current_user)
    return PrepareResponse(status=True)


@router.post("/create")
async def api_create_room(
    payload: CreatePayload,
    current_user: User = Depends(get_current_user),
    room_service: IRoomService = Depends(get_service(IRoomService))
) -> CreateResponse:
    room_iden = await room_service.create_new_room(payload.room_name, current_user.id)
    return CreateResponse(room_iden=room_iden)
