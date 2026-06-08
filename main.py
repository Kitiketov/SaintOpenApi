import asyncio

import uvicorn

from src.config.logger import setup_logging
from src.config.settings import Settings
from src.di.container import init_container
from src.infrastructure.repositories.interfaces.ISaintRepository import ISaintRepository
from src.presentation.fastapi.app import create_api_app


async def main() -> None:
    # bot = Bot(config.bot_token)
    # session = await create_http_session()
    # moderation_client = ModerationClient(
    #     base_url=str(config.api_base),
    #     session=session,
    # )
    setup_logging()
    settings = Settings()
    container = init_container(settings)
    saint_repo = container.resolve(ISaintRepository)
    await saint_repo.start_db()
    app = create_api_app()
    app.state.container = container

    config = uvicorn.Config(
        app=app,
        host=settings.api_host,
        port=settings.api_port,
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
