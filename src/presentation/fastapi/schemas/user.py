from pydantic import BaseModel


class GetRoomsResponse(BaseModel):
    rooms: dict[str, list[str]]
