from typing import Any

import httpx

from core.exceptions import (
    InvalidRoomNameException,
    TooManyRoomsException,
    RoomNotExistException,
    UserNotAdminException,
    MemberNotExistException,
)
from core.schemas.user import User
from infrastructure.api_client.exceptions import APIError

ERROR_MAP = {
    "TOO_MANY_ROOMS": lambda _: TooManyRoomsException(),
    "INVALID_ROOM_NAME": lambda _: InvalidRoomNameException(),
    "ROOM_NOT_EXISTS": lambda d: RoomNotExistException(d.get("room_name")),
    "MEMBER_NOT_EXISTS": lambda d: MemberNotExistException(d.get("room_name")),
    "USER_NOT_ADMIN": lambda d: UserNotAdminException(d.get("room_name")),
}


class RoomClient:
    def __init__(self, client: httpx.AsyncClient):
        self.client = client

    async def _request(self, method: str, url: str, **kwargs) -> dict:
        response = await self.client.request(method, url, **kwargs)

        try:
            data = response.json()
        except Exception:
            data = {}

        print("\n--- DEBUG RESPONSE ---")
        print("STATUS:", response.status_code)
        print("DATA:", data)
        print("DETAIL:", data.get("detail"))
        print("----------------------\n")

        if response.is_success:
            return data

        detail = data.get("detail")
        handler = ERROR_MAP.get(detail)

        if handler:
            raise handler(data)

        raise APIError(response.status_code, data)

    async def http_validate_room_creation(self, user: User) -> None:
        await self._request("POST", "/rooms/prepare", json={"user": user.model_dump()})

    async def http_create_room(self, room_name: str, user_id: int) -> str:
        data = await self._request("POST", "/rooms/create", json={"room_name": room_name, "user_id": user_id})

        return data["room_iden"]

    async def http_get_room_settings(
        self, room_iden: str, user_id: int, require_admin: bool
    ) -> tuple[str | bool, str | None, str | None, str | None]:
        data = await self._request(
            "GET", f"/rooms/{room_iden}/settings", params={"user_id": user_id, "require_admin": require_admin}
        )

        return data["room_name"], data["price"], data["event_time"], data["exchange_type"]

    async def http_get_room_members(self, room_iden: str, user_id: int) -> tuple[list, Any]:
        data = await self._request("GET", f"/rooms/{room_iden}/members", params={"user_id": user_id})

        return data["member_list"], data["admin"]

    async def http_get_room_access(self, room_iden: str, room_name: str) -> bool:
        data = await self._request("GET", f"/rooms/{room_iden}/access/{room_name}")

        return data["access"]
