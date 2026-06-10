from fastapi import APIRouter, Depends

from core.services.room_service import IRoomService
from presentation.fastapi.dependencies import get_service
from presentation.fastapi.schemas.room import PreparePayload, CreatePayload, PrepareResponse, CreateResponse

router = APIRouter()


@router.post("/prepare")
async def api_prepare_room(
    payload: PreparePayload, room_service: IRoomService = Depends(get_service(IRoomService))
) -> PrepareResponse:
    await room_service.prepare_create_room(payload.user)
    return PrepareResponse(status=True)


@router.post("/create")
async def api_create_room(
    payload: CreatePayload, room_service: IRoomService = Depends(get_service(IRoomService))
) -> CreateResponse:
    room_iden = await room_service.create_new_room(payload.room_name, payload.user_id)
    return CreateResponse(room_iden=room_iden)
