import httpx

from core.schemas.user import User
from infrastructure.api_client.exceptions import APITooManyRooms, APIError, APIInvalidRoomName

API_URL = "http://127.0.0.1:8000/api/rooms"


async def http_prepare_room(user: User) -> None:
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{API_URL}/prepare", json={"user": user.model_dump()})

        if response.status_code == 400:
            raise APITooManyRooms()

        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            raise APIError(response.status_code, str(e)) from e


async def http_create_room(room_name: str, user_id: int) -> str:
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{API_URL}/create", json={"room_name": room_name, "user_id": user_id})

        if response.status_code == 422:
            raise APIInvalidRoomName()

        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            raise APIError(response.status_code, str(e)) from e
        return response.json().get("room_id")
