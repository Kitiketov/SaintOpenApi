from datetime import datetime, timezone
from pydantic import BaseModel, ConfigDict, Field, HttpUrl


class TelegramLoginPayload(BaseModel):
    id: int
    first_name: str
    last_name: str | None = None
    username: str | None = None
    photo_url: HttpUrl | None = None
    auth_date: int
    hash: str

class TelegramLoginResponse(BaseModel):
    access_token: str