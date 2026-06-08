from fastapi import APIRouter, HTTPException

from presentation.fastapi.schemas.room import CreatePayload
from services import room_service

router = APIRouter(prefix="api/rooms")


@router.post("/prepare")
async def api_prepare_room(payload: CreatePayload):
    try:
        await room_service.prepare_create_room(payload.user)
        return {"status": "success"}
    except room_service.TooManyRoomsException:
        raise HTTPException(status_code=400, detail="Too many rooms")

@router.post("/create")
async def api_create_room(payload: CreatePayload):
    try:
        room_id = await room_service.create_new_room(payload.room_name, payload.user_id)
        return {"room_id": room_id}
    except room_service.InvalidRoomNameException:
        raise HTTPException(status_code=422, detail="Invalid room name")