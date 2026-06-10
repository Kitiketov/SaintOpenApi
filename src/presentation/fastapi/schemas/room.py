from pydantic import BaseModel

from core.schemas.user import User


class PreparePayload(BaseModel):
    user: User | None = None


class CreatePayload(BaseModel):
    room_name: str
    user_id: int


class PrepareResponse(BaseModel):
    status: bool


class CreateResponse(BaseModel):
    room_iden: str
