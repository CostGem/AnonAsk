from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from src.translation.translator import LocalizedTranslator

router: Router = Router(name="main_start")


@router.message(CommandStart())
async def start_command(message: Message, translator: LocalizedTranslator) -> None:
    """
    The function responds with "Hello, world" when the start command is received.

    :param translator: Translator
    :param message: The `message` parameter is of type `Message`, which represents a message received
    from a user. It contains information such as the message text, sender, chat, and other metadata
    :type message: Message
    """

    await message.answer(text=translator.get(key="start_command_message"))
