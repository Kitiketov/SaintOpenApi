from pydantic import BaseModel


class GetRoomsResponse(BaseModel):
    rooms: list[str]
