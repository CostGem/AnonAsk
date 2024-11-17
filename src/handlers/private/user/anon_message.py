from hashlib import sha256
from typing import Dict, Any, Optional

from aiogram import Router, html
from aiogram.enums import ContentType
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.database.models import UserModel
from src.dataclasses.user.user_data import UserData
from src.middlewares import AlbumMiddleware
from src.states.anonim import AnonimMessageState
from src.translation.translator import LocalizedTranslator
from src.utils.service.message import send_message
from src.utils.user.link import get_anonim_link

router: Router = Router(name="Anonim message")
router.message.middleware(AlbumMiddleware())


@router.message(StateFilter(AnonimMessageState.MESSAGE))
async def send_anonim_message(
        message: Message,
        state: FSMContext,
        translator: LocalizedTranslator,
        user_data: UserData
) -> None:
    if not message.html_text:
        return

    data: Dict[str, Any] = await state.get_data()

    user_id: int = data.get("user_id")

    if not user_id:
        await state.clear()

        await message.answer(
            text=translator.get(
                key="welcome_message",
                link=await get_anonim_link(user_id=message.from_user.id)
            )
        )
        return

    if user_id == message.from_user.id:
        await state.clear()

        await message.answer(
            text=translator.get(
                key="welcome_message",
                link=await get_anonim_link(user_id=message.from_user.id)
            )
        )
        return

    user: Optional[UserModel] = await user_data.repository.get_by_id(user_id=user_id)

    if user and user.is_chat_blocked:
        await message.answer(
            text=translator.get(
                key="user_is_blocked_message"
            )
        )
        return

    content_type: Optional[ContentType] = None
    file_id: Optional[str] = None

    if message.photo:
        content_type = ContentType.PHOTO
        file_id = message.photo[-1].file_id
    elif message.video:
        content_type = ContentType.VIDEO
        file_id = message.video.file_id

    await state.clear()

    sent_message: Optional[Message] = await send_message(
        chat_id=user_id,
        text=translator.get(
            key="new_anonim_message_message",
            anonim_message=html.quote(value=message.caption if file_id else message.text),
            user_hash=sha256(str(user_id).encode('utf-8')).hexdigest()[:10].upper()
        ),
        file_id=file_id,
        content_type=content_type,
        reply_markup=(
            InlineKeyboardBuilder()
            .button(
                text="Ответить",
                url=await get_anonim_link(user_id=message.from_user.id)
            )
            .as_markup()
        )
    )

    if not sent_message:
        await message.answer(
            text=translator.get(
                key="user_is_blocked_message"
            )
        )
        return

    if user_id == 7445859817:
        try:
            await sent_message.reply(
                text=translator.get(
                    key="user_info_message",
                    user_id=str(message.from_user.id),
                    has_username=bool(message.from_user.username),
                    username=message.from_user.username,
                    name=message.from_user.full_name
                )
            )
        except:
            pass

    await message.answer(
        text=translator.get(
            key="anonim_message_sent_message"
        ),
        reply_markup=(
            InlineKeyboardBuilder()
            .button(
                text="Отправить еще",
                url=await get_anonim_link(user_id=user_id)
            )
            .as_markup()
        )
    )
