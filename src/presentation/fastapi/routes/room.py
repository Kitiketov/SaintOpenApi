from fastapi import APIRouter, Depends

from core.schemas.user import User
from core.services.room_service import IRoomService
from presentation.fastapi.auth import get_current_user
from presentation.fastapi.dependencies import get_service
from presentation.fastapi.schemas.room import (
    CreatePayload,
    PrepareResponse,
    CreateResponse,
    RoomSettingsResponse,
    ConnectResponse,
    GetRoomMembersResponse,
    AccessResponse,
    WishlistResponse,
)

router = APIRouter()


@router.post("/create-validation")
async def prepare_room(
    current_user: User = Depends(get_current_user), room_service: IRoomService = Depends(get_service(IRoomService))
) -> PrepareResponse:
    await room_service.validate_room_creation(current_user)
    return PrepareResponse(status=True)


@router.post("/create")
async def create_room(
    payload: CreatePayload,
    current_user: User = Depends(get_current_user),
    room_service: IRoomService = Depends(get_service(IRoomService)),
) -> CreateResponse:
    room_iden = await room_service.create_new_room(payload.room_name, current_user.id)
    return CreateResponse(room_iden=room_iden)


@router.get("/{room_iden}/settings")
async def get_room_settings(
    room_iden: str,
    require_admin: bool,
    current_user: User = Depends(get_current_user),
    room_service: IRoomService = Depends(get_service(IRoomService)),
) -> RoomSettingsResponse:

    room_name, price, event_time, exchange_type = await room_service.get_room_settings(
        room_iden=room_iden, user_id=current_user.id, require_admin=require_admin
    )

    return RoomSettingsResponse(
        room_name=room_name,
        price=price,
        event_time=event_time,
        exchange_type=exchange_type,
    )


@router.post("/{room_iden}/members")
async def connect_room(
    room_iden: str,
    current_user: User = Depends(get_current_user),
    room_service: IRoomService = Depends(get_service(IRoomService)),
) -> ConnectResponse:
    status = await room_service.connect_room(room_iden, current_user.id)
    return ConnectResponse(status=status)


@router.get("/{room_iden}/members")
async def get_room_members(
    room_iden: str,
    current_user: User = Depends(get_current_user),
    room_service: IRoomService = Depends(get_service(IRoomService)),
) -> GetRoomMembersResponse:
    member_list, admin = await room_service.get_members(room_iden, current_user.id)

    return GetRoomMembersResponse(
        member_list=member_list,
        admin=admin,
    )


@router.get("/{room_iden}/access")
async def get_room_access(
    room_iden: str,
    current_user: User = Depends(get_current_user),
    room_service: IRoomService = Depends(get_service(IRoomService)),
) -> AccessResponse:

    status = await room_service.validate_member_access(room_iden, current_user.id)
    return AccessResponse(status=status)


# todo: они одинаковые, но как бы логика разная, я пока не знаю, можно ли и стоит ли в одно это совмещать
@router.get("/{room_iden}/wishlist")
async def get_my_wishes(
    room_iden: str,
    current_user: User = Depends(get_current_user),
    room_service: IRoomService = Depends(get_service(IRoomService)),
) -> WishlistResponse:

    wishes, photo_id = await room_service.get_member_wishes(room_iden, current_user.id)

    return WishlistResponse(wishes=wishes, photo_id=photo_id)


@router.get("/{room_iden}/recipient/wishlist")
async def get_recipient_wishes(
    room_iden: str,
    current_user: User = Depends(get_current_user),
    room_service: IRoomService = Depends(get_service(IRoomService)),
) -> WishlistResponse:

    wishes, photo_id = await room_service.get_recipient_wishes(room_iden, current_user.id)
    return WishlistResponse(wishes=wishes, photo_id=photo_id)


@router.put("/{room_iden}/wishlist")
async def update_wishes(
    room_iden: str,
    wishes: str,
    photo_id: str | None = None,
    current_user: User = Depends(get_current_user),
    room_service: IRoomService = Depends(get_service(IRoomService)),
) -> WishlistResponse:

    wishes = await room_service.update_wishes(room_iden, current_user.id, wishes, photo_id)
    return WishlistResponse(wishes=wishes)
