from authx import AuthX
from fastapi import APIRouter, Depends, Response

from presentation.fastapi.dependencies import get_service
from presentation.fastapi.schemas.auth import TelegramLoginPayload, TelegramLoginResponse

router = APIRouter()


@router.get("/login")
async def login(
        response: Response,
        payload: TelegramLoginPayload = Depends(),
        security: AuthX = Depends(get_service(AuthX))
) -> TelegramLoginResponse:
    # TODO тут бы проверить что это норм hash (но сон пока важнее)
    token = security.create_access_token(uid=str(payload.id))
    response.set_cookie(security.config.JWT_ACCESS_COOKIE_NAME, token)
    return TelegramLoginResponse(access_token=token)
