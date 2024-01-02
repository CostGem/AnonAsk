import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.base import BaseStorage
from aiogram.fsm.storage.redis import RedisStorage
from fastapi import FastAPI
from redis.asyncio.client import Redis
from dispatcher import get_dispatcher
from src.database import engine
from config.configuration import CONFIGURATION, Config

@webhook_server_app.
async def startup():
    """
    The above function is an event handler that runs when the application starts up and performs various
    tasks such as deleting any existing webhooks, setting up a new webhook, and initializing session
    pools.
    """

    webhook_info: WebhookInfo = await bot.get_webhook_info()

    if webhook_info.url != BOT_WEBHOOK_URL:
        await bot.set_webhook(url=BOT_WEBHOOK_URL)
    else:
        await bot.delete_webhook(drop_pending_updates=True)
        sleep(1)
        await asleep(1)
        await bot.set_webhook(url=BOT_WEBHOOK_URL)

    session_pool = await session_manager.get_pool()

    await on_startup(
        bot=bot, dispatcher=dp, scheduler=scheduler, session_pool=session_pool
    )


@webhook_server_app.post(BOT_WEBHOOK_ENDPOINT)
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
    session_pool = await session_manager.get_pool()

    await dp.feed_update(
        bot,
        update,
        session_pool=session_pool,
        scheduler=scheduler,
        wallet_api=wallet_api,
        redis=redis_instance,
    )


@webhook_server_app.on_event("shutdown")
async def shutdown():
    """
    The function `shutdown` is an event handler that is triggered when the webhook server is shutting
    down.
    """
    await on_shutdown(bot=bot, dispatcher=dp, scheduler=scheduler)


def run_webhook() -> None:
    """
    The function `run_webhook` runs a webhook server with specified configurations and registers webhook
    endpoints if wallet webhook is enabled.
    """

    if not all(
        [
            BOT_WEB_SERVER_HOST,
            BOT_WEB_SERVER_PORT != None,
            NGINX_HOST,
            BOT_WEBHOOK_ENDPOINT,
            BOT_WEBHOOK_URL,
        ]
    ):
        raise ValueError("Webhook have not been configured properly")

    if USE_WALLET_WEBHOOK:
        wallet_webhook_manager.app = webhook_server_app
        wallet_webhook_manager.register_webhook_endpoint()
        wallet_webhook_manager.failed_callbacks.append(handle_failed_event)
        wallet_webhook_manager.successful_callbacks.append(handle_successful_event)
    else:
        cprint("Payments webhook has been disabled !", "red")

    uvicorn.run(
        webhook_server_app,
        host=BOT_WEB_SERVER_HOST,
        port=BOT_WEB_SERVER_PORT,
        reload=False,
        log_level="debug" if DEVELOPING else "info",
    )


async def run_polling() -> None:
    """
    The function `run_polling` starts a polling process for a bot using the `dp` object and various
    dependencies.
    """
    session_pool = await session_manager.get_pool()

    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    if not DEVELOPING:
        await bot.delete_webhook(drop_pending_updates=True)

    await dp.start_polling(
        bot,
        session_pool=session_pool,
        scheduler=scheduler,
        redis=redis_instance,
        wallet_api=wallet_api,
    )


def start_bot() -> None:
    """
    The function `start_bot` runs either a webhook or polling based on the value of the `USE_WEBHOOK`
    variable.
    """
    try:
        if USE_WEBHOOK:
            run_webhook()
        else:
            asyncio.run(run_polling())
    except (KeyboardInterrupt, SystemExit, RuntimeError):
        pass
