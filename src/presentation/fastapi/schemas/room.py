from pydantic import BaseModel

from services.schemas.user import User


class PreparePayload(BaseModel):
    user: User | None = None

class CreatePayload(BaseModel):
    room_name: str
    user_id: int