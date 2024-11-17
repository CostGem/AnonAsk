import asyncio
from contextlib import suppress

from aiogram import Dispatcher, Bot
from dependency_injector.wiring import Provide, inject
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import async_sessionmaker

from src.config import CONFIGURATION
from src.containers.app import AppContainer
from src.database.engine import SessionMakerManager
from src.loader import on_shutdown, on_startup


@inject
async def run_polling(
        dp: Dispatcher = Provide[AppContainer.dp],
        redis: Redis = Provide[AppContainer.redis],
        bot: Bot = Provide[AppContainer.bot],
        session_manager: SessionMakerManager = Provide[AppContainer.session_manager]
) -> None:
    """Start bot polling"""

    with suppress(Exception):
        await bot.delete_webhook(drop_pending_updates=True)

    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    session_pool: async_sessionmaker = await session_manager.get_pool(
        url=CONFIGURATION.DATABASE.connection_url
    )

    await dp.start_polling(
        bot,
        session_pool=session_pool,
        redis=redis
    )


def start_bot() -> None:
    """Start the bot with polling"""

    container: AppContainer = AppContainer()
    container.init_resources()

    try:
        asyncio.run(run_polling())
    except (KeyboardInterrupt, SystemExit, RuntimeError):
        pass
