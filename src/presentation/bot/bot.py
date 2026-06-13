from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from punq import Container

from infrastructure.repositories.interfaces.ISaintRepository import ISaintRepository
from presentation.bot.handlers import create_room, settings, legacy_route
from presentation.bot.middlewares import UpdateUserMiddleware
from presentation.bot.middlewares.di_middleware import DiMiddleware


async def run_bot(token: str, container: Container) -> None:
    bot = Bot(
        token,
        default=DefaultBotProperties(parse_mode="HTML"),
    )
    dp = Dispatcher(storage=MemoryStorage())

    dp.update.middleware(DiMiddleware(container))
    # todo: хз, так ли это делается, но я пока затестить хотела (если что убрать)
    saint_repo = container.resolve(ISaintRepository)
    dp.message.middleware(UpdateUserMiddleware(saint_repo))
    dp.callback_query.middleware(UpdateUserMiddleware(saint_repo))

    dp.include_routers(
        create_room.router,
        settings.router,
        legacy_route.router
    )

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
