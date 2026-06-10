from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from presentation.bot.states import states
from presentation.bot.texts.callback_actions import CallbackAction


async def room_member_kb(room_iden):
    room_join_kb = [
        [
            InlineKeyboardButton(
                text="🎁Кому я дарю",
                callback_data=states.CallbackFactory(
                    action=CallbackAction.WHO_GIVES, room_iden=room_iden, asAdmin=False
                ).pack(),
            )
        ],
        [
            InlineKeyboardButton(
                text="✨Мои пожелания",
                callback_data=states.CallbackFactory(
                    action=CallbackAction.MY_WISHES, room_iden=room_iden, asAdmin=False
                ).pack(),
            )
        ],
        [
            InlineKeyboardButton(
                text="📄Список участников",
                callback_data=states.CallbackFactory(
                    action=CallbackAction.MEMBERS_LIST,
                    room_iden=room_iden,
                    asAdmin=False,
                ).pack(),
            )
        ],
        [
            InlineKeyboardButton(
                text="⚙️Настройки комнаты",
                callback_data=states.CallbackFactory(
                    action=CallbackAction.SHOW_ROOM_SETTINGS,
                    room_iden=room_iden,
                    asAdmin=False,
                ).pack(),
            )
        ],
        [
            InlineKeyboardButton(
                text="🚪Покинуть комнату",
                callback_data=states.CallbackFactory(
                    action=CallbackAction.LEAVE_ROOM, room_iden=room_iden, asAdmin=False
                ).pack(),
            )
        ],
        [
            InlineKeyboardButton(
                text="✉️Создать приглашение",
                callback_data=states.CallbackFactory(
                    action=CallbackAction.CREATE_INVITATION,
                    room_iden=room_iden,
                    asAdmin=False,
                ).pack(),
            )
        ],
        [
            InlineKeyboardButton(
                text="◀️Вернуться в меню",
                callback_data=states.CallbackFactory(
                    action=CallbackAction.BACK_TO_MENU,
                    room_iden=room_iden,
                    asAdmin=False,
                ).pack(),
            )
        ],
        [
            InlineKeyboardButton(
                text="🚫Закрыть окно",
                callback_data=states.CallbackFactory(
                    action=CallbackAction.CANCEL, room_iden=room_iden, asAdmin=False
                ).pack(),
            )
        ],
    ]
    return InlineKeyboardMarkup(inline_keyboard=room_join_kb)


async def wishes_kb(room_iden, asAdmin):
    confirm_kb = [
        [
            InlineKeyboardButton(
                text="✅Окей",
                callback_data=states.CallbackFactory(
                    action=CallbackAction.CANCEL, room_iden=room_iden, asAdmin=asAdmin
                ).pack(),
            ),
            InlineKeyboardButton(
                text="✏️Изменить желание",
                callback_data=states.CallbackFactory(
                    action=CallbackAction.EDIT_WISHES,
                    room_iden=room_iden,
                    asAdmin=asAdmin,
                ).pack(),
            ),
        ],
    ]
    return InlineKeyboardMarkup(inline_keyboard=confirm_kb)


async def wishes_kb2(room_iden, asAdmin):
    wishes_kb = [
        [
            InlineKeyboardButton(
                text="✅OK",
                callback_data=states.CallbackFactory(
                    action=CallbackAction.CANCEL, room_iden=room_iden, asAdmin=asAdmin
                ).pack(),
            ),
            InlineKeyboardButton(
                text="👀Посмотреть желание",
                callback_data=states.CallbackFactory(
                    action=CallbackAction.SEE_WISHES,
                    room_iden=room_iden,
                    asAdmin=asAdmin,
                ).pack(),
            ),
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=wishes_kb)
