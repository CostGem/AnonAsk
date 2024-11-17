from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.redis import RedisStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dependency_injector.containers import DeclarativeContainer, WiringConfiguration
from dependency_injector.providers import Singleton
from redis.asyncio import Redis

from src.config import CONFIGURATION
from src.database.engine import SessionMakerManager


class AppContainer(DeclarativeContainer):
    wiring_config = WiringConfiguration(
        packages=[
            "src"
        ],
    )

    bot: Singleton = Singleton(
        Bot,
        token=CONFIGURATION.BOT.TOKEN,
        default=DefaultBotProperties(
            parse_mode=CONFIGURATION.BOT.PARSE_MODE,
            link_preview_is_disabled=CONFIGURATION.BOT.DISABLE_WEB_PAGE_PREVIEW,
            protect_content=CONFIGURATION.BOT.PROTECT_CONTENT,
        ),
    )
    redis: Singleton = Singleton(
        Redis,
        host=CONFIGURATION.REDIS.HOST,
        username=CONFIGURATION.REDIS.USER,
        password=CONFIGURATION.REDIS.PASSWORD,
        port=CONFIGURATION.REDIS.PORT,
    )
    redis_storage: Singleton = Singleton(
        RedisStorage,
        redis=redis,
        state_ttl=CONFIGURATION.REDIS.STATE_TTL,
        data_ttl=CONFIGURATION.REDIS.DATA_TTL
    )

    dp: Singleton = Singleton(
        Dispatcher,
        storage=redis_storage
    )

    scheduler: Singleton = Singleton(
        AsyncIOScheduler,
        misfire_grace_time=60
    )

    session_manager: Singleton = Singleton(
        SessionMakerManager
    )
