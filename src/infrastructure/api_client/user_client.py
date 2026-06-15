import httpx

from infrastructure.api_client.exceptions import APIError

ERROR_MAP = {
    # "TOO_MANY_ROOMS": lambda _: TooManyRoomsException(),
}


class UserClient:
    def __init__(self, client: httpx.AsyncClient):
        self.client = client

    async def _request(self, method: str, url: str, **kwargs) -> dict:
        response = await self.client.request(method, url, **kwargs)

        try:
            data = response.json()
        except Exception:
            data = {}

        if response.is_success:
            return data

        detail = data.get("detail")
        handler = ERROR_MAP.get(detail)

        if handler:
            raise handler(data)

        raise APIError(response.status_code, data)

    async def http_get_rooms(self, as_admin: bool | None = None) -> dict[str, list[str]]:
        data = await self._request("GET", f"users/me/rooms", params={"as_admin": as_admin})

        return data["rooms"]
