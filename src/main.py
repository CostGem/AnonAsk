import asyncio
import time

import uvicorn
from aiogram.types import WebhookInfo, Update
from sqlalchemy.ext.asyncio import async_sessionmaker

from src.cache.redis import redis_instance
from src.config import CONFIGURATION
from src.database.engine import session_manager
from src.dispatcher_actions import on_shutdown, on_startup
from src.loader import bot, dp, webhook_server_app


@webhook_server_app.on_event("startup")
async def startup():
    """
    The above function is an event handler that runs when the application starts up and performs various
    tasks such as deleting any existing webhooks, setting up a new webhook, and initializing session
    pools.
    """

    webhook_info: WebhookInfo = await bot.get_webhook_info()

    if webhook_info.url != CONFIGURATION.BOT.webhook_url:
        await bot.set_webhook(url=CONFIGURATION.BOT.webhook_url)
    else:
        await bot.delete_webhook(drop_pending_updates=True)
        time.sleep(1)
        await bot.set_webhook(url=CONFIGURATION.BOT.webhook_url)

    await on_startup(bot=bot, dispatcher=dp)


@webhook_server_app.post(CONFIGURATION.BOT.webhook_endpoint)
async def bot_webhook(update: dict):
    """
    The above function is a webhook endpoint in a Python application that receives updates and feeds
    them to a bot for processing.

    :param update: The `update` parameter is a dictionary that contains information about the incoming
    update from the webhook. It typically includes details such as the message text, sender information,
    chat ID, etc
    :type update: dict
    """

    update: Update = Update.model_validate(update, context={"bot": bot})
    session_pool: async_sessionmaker = await session_manager.get_pool(
        url=CONFIGURATION.DATABASE.build_connection_url()
    )

    await dp.feed_update(
        bot,
        update,
        session_pool=session_pool,
        redis=redis_instance,
    )


@webhook_server_app.on_event("shutdown")
async def shutdown():
    """
    The function `shutdown` is an event handler that is triggered when the webhook server is shutting
    down.
    """
    await on_shutdown(bot=bot, dispatcher=dp)


def run_webhook() -> None:
    """
    The function `run_webhook` runs a webhook server with specified configurations and registers webhook
    endpoints if wallet webhook is enabled.
    """

    uvicorn.run(
        webhook_server_app,
        host=CONFIGURATION.BOT.webhook_host,
        port=CONFIGURATION.BOT.webhook_port,
        reload=False,
        log_level="debug" if CONFIGURATION.IS_DEVELOPMENT else "info",
    )


async def run_polling() -> None:
    """
    The function `run_polling` starts a polling process for a bot using the `dp` object and various
    dependencies.
    """

    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    session_pool: async_sessionmaker = await session_manager.get_pool(
        url=CONFIGURATION.DATABASE.build_connection_url()
    )

    if not CONFIGURATION.IS_DEVELOPMENT:
        await bot.delete_webhook(drop_pending_updates=True)

    await dp.start_polling(
        bot,
        session_pool=session_pool,
        redis=redis_instance,
    )


def start_bot() -> None:
    """
    The function `start_bot` runs either a webhook or polling based on the value of the `USE_WEBHOOK`
    variable.
    """

    try:
        if CONFIGURATION.USE_WEBHOOK:
            run_webhook()
        else:
            asyncio.run(run_polling())
    except (KeyboardInterrupt, SystemExit, RuntimeError):
        pass
