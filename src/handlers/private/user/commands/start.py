from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message, ReplyKeyboardMarkup

from src.classes.user.user_data import UserData
from src.markups.user.reply.main import get_main_keyboard
from src.translation.translator import LocalizedTranslator

router = Router(name="Start command")


@router.message(CommandStart())
async def start(
        message: Message,
        translator: LocalizedTranslator,
        user_data: UserData
) -> None:
    await user_data.repository.register(
        user_id=message.from_user.id,
        name=message.from_user.full_name,
        username=message.from_user.username
    )

    main_keyboard: ReplyKeyboardMarkup = await get_main_keyboard(translator=translator)
    await message.answer(
        text=translator.get(
            key="welcome_message",
            name=message.from_user.full_name
        ),
        reply_markup=main_keyboard
    )
