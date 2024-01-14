from datetime import datetime, timedelta
from typing import Any, Union, Dict, Optional

from aiogram.enums import MessageEntityType
from aiogram.filters import BaseFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from src.classes.types.album import Album
from src.classes.user.user_data import UserData
from src.database.repositories import CommentRepository
from src.markups.user.reply.main_menu import get_main_keyboard
from src.translation.translator import LocalizedTranslator


class CommentFilter(BaseFilter):
    """Comment filter"""

    async def __call__(
            self,
            message: Message,
            state: FSMContext,
            translator: LocalizedTranslator,
            user_data: UserData,
            session: AsyncSession,
            album: Optional[Album] = None
    ) -> Union[bool, Dict[str, Any]]:
        if user_data.user.is_banned:
            await state.clear()
            main_keyboard = await get_main_keyboard(translator=translator)
            await message.answer(
                text=translator.get(key="you_blocked"),
                reply_markup=main_keyboard
            )
            return False

        comment_repository: CommentRepository = CommentRepository(session=session)
        last_comment = await comment_repository.get_last_comment(user=user_data.user)

        if last_comment:
            if datetime.utcnow() <= last_comment.commented_at + timedelta(seconds=30):
                await state.clear()
                main_keyboard = await get_main_keyboard(translator=translator)
                await message.answer(
                    text=translator.get("commenting_cooldown_message"),
                    reply_markup=main_keyboard
                )
                return False

        if album:
            await message.answer(
                text=translator.get(key="can_only_attach_one_attachment_message")
            )
            return False

        if not message.photo and not message.html_text and not message.sticker and not message.video:
            await message.answer(
                text=translator.get(key="attachments_are_not_supported_message")
            )
            return False

        if message.entities:
            for entity in message.entities:
                if entity.type in (
                        MessageEntityType.URL,
                        MessageEntityType.TEXT_LINK,
                        MessageEntityType.MENTION,
                        MessageEntityType.TEXT_MENTION
                ):
                    await message.answer(
                        text=translator.get(key="links_are_prohibited_message")
                    )
                    return False
        return True
