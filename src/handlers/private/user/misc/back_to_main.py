from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.filters import KeyboardButtonFilter
from src.markups.user.reply.main_menu import get_main_keyboard
from src.translation.translator import LocalizedTranslator

router = Router(name="Back to main menu")


@router.message(KeyboardButtonFilter(key="back_to_main_button_text"))
async def back_to_main_menu(message: Message, state: FSMContext, translator: LocalizedTranslator) -> None:
    await state.clear()

    main_keyboard = await get_main_keyboard(translator=translator)
    await message.answer(
        text=translator.get(key="back_to_main_message"),
        reply_markup=main_keyboard
    )
