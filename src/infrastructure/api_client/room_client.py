import httpx

from core.exceptions import InvalidRoomNameException, TooManyRoomsException, RoomNotExistException, \
    UserNotAdminException, MemberNotExistException
from core.schemas.user import User
from infrastructure.api_client.exceptions import APIError


class RoomClient:
    def __init__(self, client: httpx.AsyncClient):
        self.client = client

    async def http_prepare_room(self, user: User) -> None:
        response = await self.client.post("/rooms/prepare", json={"user": user.model_dump()})

        if response.status_code == 400:
            raise TooManyRoomsException()

        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            raise APIError(response.status_code, str(e)) from e

    async def http_create_room(self, room_name: str, user_id: int) -> str:
        response = await self.client.post("/rooms/create", json={"room_name": room_name, "user_id": user_id})

        if response.status_code == 422:
            raise InvalidRoomNameException()

        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            raise APIError(response.status_code, str(e)) from e
        return response.json()["room_iden"]

    async def http_get_room_settings(self, room_iden: str, user_id: int, require_admin: bool) -> tuple[str | bool, str | None, str | None, str | None]:
        response = await self.client.get(
            f"/rooms/{room_iden}/settings",
            params={"user_id": user_id, "require_admin": require_admin}
        )

        if response.status_code in (403, 404):
            error_data = response.json()
            error_detail = error_data.get("detail")
            room_name = error_data.get("room_name", "Неизвестная комната")

            if error_detail == "ROOM_NOT_EXISTS":
                raise RoomNotExistException(room_name=room_name)
            elif error_detail == "USER_NOT_ADMIN":
                raise UserNotAdminException(room_name=room_name)
            elif error_detail == "MEMBER_NOT_EXISTS":
                raise MemberNotExistException(room_name=room_name)

        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            raise APIError(response.status_code, str(e)) from e

        data = response.json()
        return data["room_name"], data["price"], data["event_time"], data["exchange_type"]