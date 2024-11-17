from aiogram import Router
from aiogram.types import CallbackQuery

from src.factories.service.empty import EmptyFactory

router: Router = Router(name="Empty callback")


@router.callback_query(EmptyFactory.filter())
async def handle_empty_callback(call: CallbackQuery) -> None:
    await call.answer()
