from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

router: Router = Router(name="main_start")


@router.message(CommandStart())
async def start_command(message: Message) -> None:
    """
    The function responds with "Hello, world" when the start command is received.

    :param message: The `message` parameter is of type `Message`, which represents a message received
    from a user. It contains information such as the message text, sender, chat, and other metadata
    :type message: Message
    """
    await message.answer("Hello, world")
