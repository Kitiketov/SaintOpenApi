import httpx
from services.schemas.user import User

API_URL = "http://127.0.0.1:8000/api/rooms"
class APIError(Exception): pass
class APITooManyRooms(APIError): pass
class APIInvalidRoomName(APIError): pass


async def http_prepare_room(user: User) -> None:
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{API_URL}/prepare", json={"user": user})

        if response.status_code == 400:
            raise APITooManyRooms()

        response.raise_for_status()

async def http_create_room(room_name: str, user_id: int) -> str:
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{API_URL}/create", json={"room_name": room_name, "user_id": user_id})

        if response.status_code == 422:
            raise APIInvalidRoomName()

        response.raise_for_status()
        return response.json().get("room_id")