from aiogram import Router
from aiogram.filters import ChatMemberUpdatedFilter, KICKED, MEMBER
from aiogram.types import ChatMemberUpdated

from src.dataclasses.user.user_data import UserData

router: Router = Router(name="Chat block router")


@router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=KICKED))
async def user_blocked_bot(_: ChatMemberUpdated, user_data: UserData):
    if user_data.user:
        await user_data.repository.set_chat_blocked(
            user=user_data.user,
            chat_blocked=True
        )


@router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=MEMBER))
async def user_unblocked_bot(_: ChatMemberUpdated, user_data: UserData):
    if user_data.user:
        await user_data.repository.set_chat_blocked(
            user=user_data.user,
            chat_blocked=False
        )
