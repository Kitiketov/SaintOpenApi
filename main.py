import asyncio

import uvicorn
from aiogram import Bot

from infrastructure.db import db
from infrastructure.settings import settings
from presentation.fastapi.app import create_api_app


async def main() -> None:
    await db.start_db()
    #bot = Bot(settings.bot_token)
    # session = await create_http_session()
    # moderation_client = ModerationClient(
    #     base_url=str(settings.api_base),
    #     session=session,
    # )
    app = create_api_app()
    
    config = uvicorn.Config(
        app=app,
        host=settings.notify_host,
        port=settings.notify_port,
        log_level="info",
    )
    server = uvicorn.Server(config)
    api_task = asyncio.create_task(server.serve())

    try:
        pass
    #     await run_bot(bot, moderation_client)
    finally:
    #     server.should_exit = True
         await api_task
    #     await session.close()
    #     await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
