from typing import Union
from aiogram import Bot, Dispatcher, Router
from aiogram.fsm.storage.redis import RedisStorage
from fastapi import FastAPI

from app.cache.redis_service import redis_instance
from aiogram import Dispatcher
from aiogram.fsm.storage.base import BaseEventIsolation, BaseStorage
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.fsm.strategy import FSMStrategy
from redis.asyncio.client import Redis

from src.config.configuration import CONFIGURATION, Config
from src.dispatcher_actions import on_shutdown, on_startup
from src.handlers import router


def get_dispatcher():
    redis_storage = RedisStorage(
        redis=redis_instance,
        state_ttl=CONFIGURATION.REDIS.state_ttl,
        data_ttl=CONFIGURATION.REDIS.data_ttl,
    )

    dp: Dispatcher = Dispatcher(storage=redis_storage)
    dp.include_router(router)

    dp.startup.register(callback=on_startup)
    dp.shutdown.register(callback=on_shutdown)

    return dp


bot: Bot = Bot(
    token=CONFIGURATION.BOT.token,
    session=CONFIGURATION.BOT.session,
    parse_mode=CONFIGURATION.BOT.parse_mode,
    disable_web_page_preview=CONFIGURATION.BOT.disable_web_page_preview,
    protect_content=CONFIGURATION.BOT.protect_content,
)
dp: Dispatcher = get_dispatcher()
webhook_server_app: FastAPI = FastAPI()
