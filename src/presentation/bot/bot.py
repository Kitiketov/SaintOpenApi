from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage

from presentation.bot.handlers import create_room
from presentation.bot.middlewares import UpdateUserMiddleware


async def run_bot(token: str) -> None:

    bot = Bot(
        token,
        default=DefaultBotProperties(parse_mode="HTML"),
    )
    dp = Dispatcher(storage=MemoryStorage())
    dp.message.middleware(UpdateUserMiddleware())
    dp.callback_query.middleware(UpdateUserMiddleware())

    dp.include_routers(
        create_room.router,
    )

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
