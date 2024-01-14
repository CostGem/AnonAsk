from typing import Optional

from aiogram import Router, F, html
from aiogram.filters import Command
from aiogram.types import Message, PhotoSize, Video, Animation

from src.translation.translator import LocalizedTranslator

router = Router(name="File command")


@router.message(Command(commands=["file"]), F.photo | F.video | F.animation)
async def file_information(message: Message, translator: LocalizedTranslator) -> None:
    media: Optional[PhotoSize, Video, Animation] = None
    if message.photo:
        media = message.photo[-1]
    elif message.video:
        media = message.video
    elif message.animation:
        media = message.animation

    await message.reply(
        text=translator.get(
            key="file_info_message",
            file_id=html.code(value=media.file_id),
            height=media.height,
            width=media.width,
            file_size=media.file_size
        )
    )
