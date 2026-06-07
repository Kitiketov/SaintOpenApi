from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage


async def run_bot(token: str) -> None:
    
    bot = Bot(
        token,
        default=DefaultBotProperties(parse_mode="HTML"),
    )
    dp = Dispatcher(storage=MemoryStorage())
    dp.message.middleware(UpdateUserMiddleware())
    dp.callback_query.middleware(UpdateUserMiddleware())

    dp.include_routers(
        legacy_route.router,
        common.router,
        info.router,
        wishes.router,
        room_admin.router,
        create_room.router,
        custom_invation.router,
        invitation.router,
        debug.router,
        join_room.router,
        room_settings.router,
        admin_command.router,
    )

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
