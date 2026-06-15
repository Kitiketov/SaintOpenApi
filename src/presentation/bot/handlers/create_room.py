from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from core.exceptions import TooManyRoomsException, InvalidRoomNameException
from core.schemas.user import User
from infrastructure.api_client.exceptions import APIError
from infrastructure.api_client.room_client import RoomClient
from presentation.bot.handlers.common import set_reaction
from presentation.bot.keyboards import common_kb, room_admin_kb
from presentation.bot.states.states import CallbackFactory, Gen
from presentation.bot.texts import messages
from presentation.bot.texts.callback_actions import CallbackAction

router = Router(name=__name__)


@router.callback_query(CallbackFactory.filter(F.action == CallbackAction.CREATE_ROOM))
async def start_create_room(
    call: CallbackQuery,
    state: FSMContext,
    room_client: RoomClient,
):
    user = User(
        id=call.from_user.id,
        first_name=call.from_user.first_name,
        last_name=call.from_user.last_name,
        username=call.from_user.username,
    )

    try:
        await room_client.http_validate_room_creation(user)
    except TooManyRoomsException:
        await call.message.answer(
            messages.too_many_rooms(),
            reply_markup=await common_kb.cancel_kb("None", False),
        )
        return
    except APIError:
        await call.message.answer("Ошибка сервера")
        return

    await state.set_state(Gen.room_name_to_create)
    await call.message.answer(
        messages.prompt_create_room_name(),
        reply_markup=await common_kb.cancel_kb("None", False),
    )


@router.message(Gen.room_name_to_create)
async def create_room(msg: Message, state: FSMContext, room_client: RoomClient):
    room_name = msg.text

    if msg.text == "🚫Отмена":
        await state.clear()
        await msg.answer(messages.menu(), reply_markup=common_kb.choice_kb)
        return

    try:
        room_iden = await room_client.http_create_room(room_name, msg.from_user.id)
    except InvalidRoomNameException:
        await msg.answer(
            messages.invalid_room_name(),
            reply_markup=await common_kb.cancel_kb("None", False),
        )
        return
    except APIError:
        await msg.answer("Ошибка сервера")
        return

    await state.clear()
    kb = await room_admin_kb.room_admin_kb(f"{room_iden}")
    await set_reaction(msg)
    await msg.answer(
        messages.room_created(room_name, room_iden),
        reply_markup=kb,
    )
