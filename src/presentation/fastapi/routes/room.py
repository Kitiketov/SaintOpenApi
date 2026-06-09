from abc import ABC, abstractmethod

from fastapi import APIRouter, HTTPException, Depends, Request

from core.exceptions import TooManyRoomsException, InvalidRoomNameException
from core.schemas.user import User
from infrastructure.repositories.interfaces import ISaintRepository
from presentation.fastapi.dependencies import get_service
from presentation.fastapi.schemas.room import PreparePayload, CreatePayload

#todo: ощущение, что здесь будет дофига кода и надо бы это в отдельный файл скинуть типо в core, хз?
class IRoomRepository(ABC):
    @abstractmethod
    async def prepare_create_room(self, user: User) -> None:
        pass

    @abstractmethod
    async def create_new_room(self, room_name: str, user_id: int) -> str:
        pass


class RoomRepository(IRoomRepository):
    def __init__(self, saint_repo: ISaintRepository):
        self.saint_repo = saint_repo

    async def prepare_create_room(self, user: User) -> None:
        room_count = await self.saint_repo.count_user_room(user.id)

        if room_count > 5:
            raise TooManyRoomsException()

        await self.saint_repo.add_user(user)

    async def create_new_room(self, room_name: str, user_id: int) -> str:
        room_id = await self.saint_repo.create_room(room_name, user_id)

        if not room_id:
            raise InvalidRoomNameException()

        return room_id


router = APIRouter(prefix="rooms")


@router.post("/prepare")
async def api_prepare_room(
    payload: PreparePayload, request: Request, room_repo: IRoomRepository = Depends(get_service(IRoomRepository))
):
    try:
        await room_repo.prepare_create_room(payload.user)
        return {"status": "success"}
    except TooManyRoomsException:
        raise HTTPException(status_code=400, detail="Too many rooms")


@router.post("/create")
async def api_create_room(
    payload: CreatePayload, request: Request, room_repo: IRoomRepository = Depends(get_service(IRoomRepository))
):
    try:
        room_id = await room_repo.create_new_room(payload.room_name, payload.user_id)
        return {"room_id": room_id}
    except InvalidRoomNameException:
        raise HTTPException(status_code=422, detail="Invalid room name")
