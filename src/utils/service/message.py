import logging
from typing import Union, Optional

from aiogram import Bot
from aiogram.enums import ContentType
from aiogram.exceptions import TelegramBadRequest, TelegramForbiddenError
from aiogram.types import Message, InlineKeyboardMarkup
from dependency_injector.wiring import inject, Provide

from src.containers.app import AppContainer


async def delete_message(message: Message) -> None:
    """
    Delete a message

    :param message: Message to delete
    """

    try:
        await message.delete()
    except (TelegramBadRequest, TelegramForbiddenError):
        pass
    except Exception as ex:
        logging.error(f"Error while deleting message: {ex}")


@inject
async def send_message(
        chat_id: Union[int, str],
        text: str,
        file_id: Optional[str] = None,
        content_type: Optional[ContentType] = None,
        bot: Bot = Provide[AppContainer.bot],
        reply_markup: Optional[InlineKeyboardMarkup] = None
) -> Optional[Message]:
    """
    Send a message with an optional media

    :param chat_id: Chat ID to send message to
    :param text: Message text
    :param file_id: File ID for media
    :param content_type: Content type for media
    :param bot: Bot instance
    :param reply_markup: Inline keyboard markup
    :return: Sent message if successful, otherwise None
    """

    sent_message: Optional[Message] = None

    try:
        if not content_type and not file_id:
            sent_message = await bot.send_message(
                chat_id=chat_id,
                text=text,
                reply_markup=reply_markup
            )
            return sent_message

        if content_type == ContentType.PHOTO:
            sent_message = await bot.send_photo(
                chat_id=chat_id,
                photo=file_id,
                caption=text,
                reply_markup=reply_markup
            )
        elif content_type == ContentType.VIDEO:
            sent_message = await bot.send_video(
                chat_id=chat_id,
                video=file_id,
                caption=text,
                reply_markup=reply_markup
            )
    except Exception as ex:
        logging.error(f"Error while sending message: {ex}")

    return sent_message
