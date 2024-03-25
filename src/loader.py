from contextlib import asynccontextmanager

from aiogram import Bot
from aiogram import Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import WebhookInfo
from apscheduler.executors.asyncio import AsyncIOExecutor
from apscheduler.jobstores.redis import RedisJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import FastAPI

from src.cache.redis import redis_instance
from src.config import CONFIGURATION
from src.dispatcher_actions import on_shutdown
from src.handlers import router


def get_dispatcher():
    """
    Create and configures a dispatcher for handling requests,
    using a Redis storage backend
    """

    redis_storage = RedisStorage(
        redis=redis_instance,
        state_ttl=CONFIGURATION.REDIS.state_ttl,
        data_ttl=CONFIGURATION.REDIS.data_ttl,
    )

    dispatcher: Dispatcher = Dispatcher(storage=redis_storage)
    dispatcher.include_router(router)

    return dispatcher


def get_scheduler() -> AsyncIOScheduler:
    """Returns a scheduler"""

    scheduler: AsyncIOScheduler = AsyncIOScheduler()
    scheduler.add_executor(executor=AsyncIOExecutor())
    scheduler.add_jobstore(
        jobstore=RedisJobStore(
            username=CONFIGURATION.REDIS.username,
            password=CONFIGURATION.REDIS.password,
            host=CONFIGURATION.REDIS.host,
            port=CONFIGURATION.REDIS.port
        )
    )

    return scheduler


@asynccontextmanager
async def lifespan(app: FastAPI):
    webhook_info: WebhookInfo = await bot.get_webhook_info()

    if webhook_info.url != CONFIGURATION.BOT.webhook_url:
        await bot.set_webhook(url=CONFIGURATION.BOT.webhook_url)
    else:
        await bot.delete_webhook(drop_pending_updates=True)
        # time.sleep(1)
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
