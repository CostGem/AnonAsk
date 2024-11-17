from aiogram import Bot
from aiogram.types import User
from aiogram.utils.payload import encode_payload
from dependency_injector.wiring import inject, Provide

from src.containers.app import AppContainer


@inject
async def get_anonim_link(user_id: int, bot: Bot = Provide[AppContainer.bot]) -> str:
    current_bot: User = await bot.get_me()

    payload: str = encode_payload(payload=str(user_id))

    return f"https://t.me/{current_bot.username}?start={payload}"
