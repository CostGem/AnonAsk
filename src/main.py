import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.base import BaseStorage
from aiogram.fsm.storage.redis import RedisStorage
from redis.asyncio.client import Redis

from config.configuration import Config


async def startup(dispatcher: Dispatcher, bot: Bot) -> None:
    """Bot startup"""

    pass


async def shutdown(dispatcher: Dispatcher, bot: Bot) -> None:
    """Bot shutdown"""

    await bot.session.close()
    await dispatcher.storage.close()


async def main() -> None:
    """Application startup"""

    CONFIGURATION = Config()

    logging.basicConfig(level=CONFIGURATION.LOGGING_LEVEL)

    redis_instance = Redis(
        host=CONFIGURATION.REDIS.host,
        username=CONFIGURATION.REDIS.username,
        password=CONFIGURATION.REDIS.password,
        port=CONFIGURATION.REDIS.port
    )
    storage: BaseStorage = RedisStorage(
        redis=redis_instance,
        state_ttl=CONFIGURATION.REDIS.state_ttl,
        data_ttl=CONFIGURATION.REDIS.data_ttl
    )
    bot: Bot = Bot(
        token=CONFIGURATION.BOT.token,
        session=CONFIGURATION.BOT.session,
        parse_mode=CONFIGURATION.BOT.parse_mode,
        disable_web_page_preview=CONFIGURATION.BOT.disable_web_page_preview,
        protect_content=CONFIGURATION.BOT.protect_content
    )
    dp: Dispatcher = Dispatcher(storage=storage)

    dp.startup.register(startup)
    dp.shutdown.register(shutdown)

    await dp.start_polling(bot, redis=redis_instance)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
