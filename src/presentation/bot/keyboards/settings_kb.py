from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from presentation.bot.states import states
from presentation.bot.texts.callback_actions import CallbackAction


async def settings_view_kb(room_iden, asAdmin=True):
    row = [
        InlineKeyboardButton(
            text="✅Окей",
            callback_data=states.CallbackFactory(
                action=CallbackAction.CANCEL, room_iden=room_iden, asAdmin=asAdmin
            ).pack(),
        )
    ]
    if asAdmin:
        row.append(
            InlineKeyboardButton(
                text="✏️Редактировать",
                callback_data=states.CallbackFactory(
                    action=CallbackAction.OPEN_ROOM_SETTINGS_EDIT,
                    room_iden=room_iden,
                    asAdmin=asAdmin,
                ).pack(),
            )
        )
    return InlineKeyboardMarkup(inline_keyboard=[row])


async def settings_edit_kb(room_iden, asAdmin=True):
    kb = [
        [
            InlineKeyboardButton(
                text="💰Диапазон стоимости",
                callback_data=states.CallbackFactory(
                    action=CallbackAction.EDIT_ROOM_PRICE,
                    room_iden=room_iden,
                    asAdmin=asAdmin,
                ).pack(),
            )
        ],
        [
            InlineKeyboardButton(
                text="🗓Время проведения",
                callback_data=states.CallbackFactory(
                    action=CallbackAction.EDIT_ROOM_TIME,
                    room_iden=room_iden,
                    asAdmin=asAdmin,
                ).pack(),
            )
        ],
        [
            InlineKeyboardButton(
                text="🎁Тип обмена",
                callback_data=states.CallbackFactory(
                    action=CallbackAction.EDIT_ROOM_TYPE,
                    room_iden=room_iden,
                    asAdmin=asAdmin,
                ).pack(),
            )
        ],
        [
            InlineKeyboardButton(
                text="◀️Назад",
                callback_data=states.CallbackFactory(
                    action=CallbackAction.EDIT_ROOM_SETTINGS,
                    room_iden=room_iden,
                    asAdmin=asAdmin,
                ).pack(),
            ),
            InlineKeyboardButton(
                text="🚫Отмена",
                callback_data=states.CallbackFactory(
                    action=CallbackAction.CANCEL, room_iden=room_iden, asAdmin=asAdmin
                ).pack(),
            ),
        ],
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)


async def settings_type_kb(room_iden, asAdmin=True):
    kb = [
        [
            InlineKeyboardButton(
                text="🎄Централизованый",
                callback_data=states.CallbackFactory(
                    action=CallbackAction.SET_ROOM_TYPE_CENTRAL,
                    room_iden=room_iden,
                    asAdmin=asAdmin,
                ).pack(),
            )
        ],
        [
            InlineKeyboardButton(
                text="🎁Подброс подарка",
                callback_data=states.CallbackFactory(
                    action=CallbackAction.SET_ROOM_TYPE_THROW,
                    room_iden=room_iden,
                    asAdmin=asAdmin,
                ).pack(),
            )
        ],
        [
            InlineKeyboardButton(
                text="◀️Назад",
                callback_data=states.CallbackFactory(
                    action=CallbackAction.OPEN_ROOM_SETTINGS_EDIT,
                    room_iden=room_iden,
                    asAdmin=asAdmin,
                ).pack(),
            ),
            InlineKeyboardButton(
                text="🚫Отмена",
                callback_data=states.CallbackFactory(
                    action=CallbackAction.CANCEL, room_iden=room_iden, asAdmin=asAdmin
                ).pack(),
            ),
        ],
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)
