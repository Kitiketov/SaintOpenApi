import httpx

from infrastructure.api_client.exceptions import APIError


class UserClient:
    def __init__(self, client: httpx.AsyncClient):
        self.client = client

    async def http_get_rooms(self, user_id: int, as_admin: bool) -> list[str]:
        response = await self.client.get(f"users/{user_id}/rooms", params={"as_admin": as_admin})

        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            raise APIError(response.status_code, str(e)) from e

        return response.json()["rooms"]
