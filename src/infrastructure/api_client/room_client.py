import httpx

from core.schemas.user import User
from infrastructure.api_client.exceptions import APITooManyRooms, APIError, APIInvalidRoomName


class RoomClient:
    def __init__(self, client: httpx.AsyncClient):
        self.client = client

    async def http_prepare_room(self, user: User) -> None:
        response = await self.client.post("/rooms/prepare", json={"user": user.model_dump()})

        if response.status_code == 400:
            raise APITooManyRooms()

        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            raise APIError(response.status_code, str(e)) from e

    async def http_create_room(self, room_name: str, user_id: int) -> str:
        response = await self.client.post("/rooms/create", json={"room_name": room_name, "user_id": user_id})

        if response.status_code == 422:
            raise APIInvalidRoomName()

        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            raise APIError(response.status_code, str(e)) from e
        return response.json()["room_iden"]
