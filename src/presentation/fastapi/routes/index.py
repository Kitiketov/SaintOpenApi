from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse

from config.settings import Settings
from presentation.fastapi.dependencies import get_service

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def login_page(
        request: Request,
        settings: Settings = Depends(get_service(Settings)),
) -> HTMLResponse:
    return request.app.state.templates.TemplateResponse(
        request=request,
        name="login.html",
        context={
            "bot_name": "pylt_ot_iderka_bot",
            "auth_url": f"https://{settings.ngrok_host}/api/auth/login",
        },
    )
