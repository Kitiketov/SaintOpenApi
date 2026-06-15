from pydantic import BaseModel

from core.schemas.user import User


class CreatePayload(BaseModel):
    room_name: str


class PrepareResponse(BaseModel):
    status: bool


class CreateResponse(BaseModel):
    room_iden: str


class RoomSettingsResponse(BaseModel):
    room_name: str | bool
    price: str | None
    event_time: str | None
    exchange_type: str | None


class ConnectResponse(BaseModel):
    status: bool


class ConnectPayload(BaseModel):
    room_iden: str


class GetRoomMembersResponse(BaseModel):
    member_list: list[User]
    admin: User
