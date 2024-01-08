import time
from contextlib import asynccontextmanager

from aiogram import Bot
from aiogram import Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import WebhookInfo
from fastapi import FastAPI

from src.cache.redis import redis_instance
from src.config import CONFIGURATION
from src.dispatcher_actions import on_shutdown, on_startup
from src.handlers import router


def get_dispatcher():
    """
    The function `get_dispatcher` creates and configures a `Dispatcher` object for handling requests,
    using a Redis storage backend.
    :return: an instance of the `Dispatcher` class.
    """

    redis_storage = RedisStorage(
        redis=redis_instance,
        state_ttl=CONFIGURATION.REDIS.state_ttl,
        data_ttl=CONFIGURATION.REDIS.data_ttl,
    )

    dispatcher: Dispatcher = Dispatcher(storage=redis_storage)
    dispatcher.include_router(router)

    dispatcher.startup.register(callback=on_startup)
    dispatcher.shutdown.register(callback=on_shutdown)

    return dispatcher


@asynccontextmanager
async def lifespan(app: FastAPI):
    webhook_info: WebhookInfo = await bot.get_webhook_info()

    if webhook_info.url != CONFIGURATION.BOT.webhook_url:
        await bot.set_webhook(url=CONFIGURATION.BOT.webhook_url)
    else:
        await bot.delete_webhook(drop_pending_updates=True)
        time.sleep(1)
        await bot.set_webhook(url=CONFIGURATION.BOT.webhook_url)

    yield
    await on_shutdown(bot=bot, dispatcher=dp)


bot: Bot = Bot(
    token=CONFIGURATION.BOT.token,
    session=CONFIGURATION.BOT.session,
    parse_mode=CONFIGURATION.BOT.parse_mode,
    disable_web_page_preview=CONFIGURATION.BOT.disable_web_page_preview,
    protect_content=CONFIGURATION.BOT.protect_content,
)

dp: Dispatcher = get_dispatcher()

webhook_server_app: FastAPI = FastAPI(lifespan=lifespan)
