from aiogram import Router
from aiogram.types import Message, CallbackQuery

from src.classes.user.user_data import UserData
from src.factories.profile import ProfileFactory
from src.filters import KeyboardButtonFilter
from src.markups.user.inline.profile import get_profile_menu
from src.translation.translator import LocalizedTranslator

router = Router(name="Profile")


@router.message(KeyboardButtonFilter(key="profile_button_text"))
async def user_profile(message: Message, translator: LocalizedTranslator, user_data: UserData) -> None:
    profile_menu = await get_profile_menu(user=user_data.user, translator=translator)
    await message.answer(
        text=translator.get(
            key="profile_message",
            user_id=user_data.user.id,
            have_nickname=bool(user_data.user.nickname),
            nickname=user_data.user.nickname,
            status_emoji=user_data.status.emoji,
            role_name=user_data.role.name,
            register_date=user_data.user.register_date.strftime("%d.%m.%Y")
        ),
        reply_markup=profile_menu
    )


@router.callback_query(ProfileFactory().filter())
async def to_user_profile(call: CallbackQuery, translator: LocalizedTranslator, user_data: UserData) -> None:
    profile_menu = await get_profile_menu(user=user_data.user, translator=translator)
    await call.message.edit_text(
        text=translator.get(
            key="profile_message",
            user_id=user_data.user.id,
            have_nickname=bool(user_data.user.nickname),
            nickname=user_data.user.nickname,
            status_emoji=user_data.status.emoji,
            role_name=user_data.role.name,
            register_date=user_data.user.register_date.strftime("%d.%m.%Y")
        ),
        reply_markup=profile_menu
    )
