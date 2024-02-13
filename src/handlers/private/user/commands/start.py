from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from src.translation.translator import LocalizedTranslator

router = Router(name="Start command")


@router.message(CommandStart())
async def start(message: Message, translator: LocalizedTranslator) -> None:
    await message.answer(
        text=translator.get(key="welcome_message")
    )
