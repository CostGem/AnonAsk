import logging
from asyncio import sleep
from typing import Optional, Union

from aiogram import Bot
from aiogram.exceptions import TelegramRetryAfter
from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, Video, Sticker, PhotoSize


from src.database.repositories import UserRepository
from src.translation.translator import LocalizedTranslator


async def send_message(
        bot: Bot,
        chat_id: int,
        text: Optional[str],
        photo: Optional[PhotoSize] = None,
        video: Optional[Video] = None,
        sticker: Optional[Sticker] = None,
        reply_message_id: Optional[int] = None,
        reply_markup: Optional[Union[ReplyKeyboardMarkup, InlineKeyboardMarkup]] = None
) -> int:
    """
    Send message to user and return message id

    :param bot: Bot
    :param chat_id: Chat ID
    :param text: Message text
    :param photo: Photo
    :param video: Video
    :param sticker: Sticker
    :param reply_message_id: Reply message ID
    :param reply_markup: Keyboard
    """

    if photo:
        message = await bot.send_photo(
            chat_id=chat_id,
            photo=photo[-1].file_id,
            caption=text,
            reply_to_message_id=reply_message_id,
            reply_markup=reply_markup
        )
    elif video:
        message = await bot.send_video(
            chat_id=chat_id,
            video=video.file_id,
            caption=text,
            reply_to_message_id=reply_message_id,
            reply_markup=reply_markup
        )
    elif sticker:
        message = await bot.send_sticker(
            chat_id=chat_id,
            sticker=sticker.file_id,
            reply_to_message_id=reply_message_id,
            reply_markup=reply_markup,
        )
    else:
        message = await bot.send_message(
            chat_id=chat_id,
            text=text,
            reply_to_message_id=reply_message_id,
            reply_markup=reply_markup,
            disable_web_page_preview=True
        )

    return message.message_id


async def send_for_all_users(
        translator: LocalizedTranslator,
        user_repository: UserRepository,
        bot: Bot,
        admin_id: int,
        text: Optional[str],
        photo: Optional[PhotoSize] = None,
        video: Optional[Video] = None,
        reply_markup: Optional[Union[ReplyKeyboardMarkup, InlineKeyboardMarkup]] = None
) -> None:
    """
    Send message to all users

    :param translator: Translator
    :param user_repository: UserRepository
    :param bot: Bot
    :param admin_id: Admin ID
    :param text: Message text
    :param photo: Photo
    :param video: Video
    :param reply_markup: Keyboard
    """

    statistic_message = await bot.send_message(
        chat_id=admin_id,
        text=translator.get(key="mailing_started_message")
    )

    users_count = await user_repository.get_not_bot_blocked_users_count()
    success_messages_count: int = 0
    fail_messages_count: int = 0

    for offset in range(0, users_count, 300):
        users = await user_repository.get_not_bot_blocked_users(admin_id=admin_id, offset=offset, limit=300)
        for user in users:
            try:
                await send_message(
                    bot=bot,
                    chat_id=user.user_id,
                    text=text,
                    photo=photo,
                    video=video,
                    reply_markup=reply_markup
                )

                success_messages_count += 1
                if success_messages_count % 50 == 0:
                    await statistic_message.edit_text(
                        text=translator.get(
                            key="mailing_statistics_message",
                            success_messages_count=success_messages_count,
                            fail_messages_count=fail_messages_count
                        )
                    )
            except Exception as ex:
                logging.error(msg=ex, exc_info=True)
                fail_messages_count += 1

    await statistic_message.edit_text(
        text=translator.get(
            key="mailing_end_message",
            success_messages_count=success_messages_count,
            fail_messages_count=fail_messages_count
        )
    )
