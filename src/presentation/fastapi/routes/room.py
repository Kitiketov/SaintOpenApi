from fastapi import APIRouter, Depends, Request

from core.services.room_service import IRoomService

from presentation.fastapi.dependencies import get_service
from presentation.fastapi.schemas.room import PreparePayload, CreatePayload

router = APIRouter()


@router.post("/prepare")
async def api_prepare_room(
    payload: PreparePayload, request: Request, room_repo: IRoomService = Depends(get_service(IRoomService))
):
    await room_repo.prepare_create_room(payload.user)
    return {"status": "success"}


@router.post("/create")
async def api_create_room(
    payload: CreatePayload, request: Request, room_repo: IRoomService = Depends(get_service(IRoomService))
):
    room_id = await room_repo.create_new_room(payload.room_name, payload.user_id)
    return {"room_id": room_id}
