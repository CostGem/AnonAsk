import asyncio

import uvicorn
from aiogram.types import Update
from sqlalchemy.ext.asyncio import async_sessionmaker

from src.cache.redis import redis_instance
from src.config import CONFIGURATION
from src.database.engine import session_manager
from src.dispatcher_actions import on_shutdown, on_startup
from src.loader import bot, dp, webhook_server_app


@webhook_server_app.post(CONFIGURATION.BOT.webhook_endpoint)
async def bot_webhook(update: dict):
    """Bot webhook endpoint"""

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


def run_webhook() -> None:
    """Run webhook server"""

    uvicorn.run(
        webhook_server_app,
        host=CONFIGURATION.BOT.webhook_host,
        port=CONFIGURATION.BOT.webhook_port,
        reload=False,
        log_level="debug" if CONFIGURATION.IS_DEVELOPMENT else "info",
    )


async def run_polling() -> None:
    """Start bot polling"""

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
    """Start the bot with polling or webhook"""

    try:
        if CONFIGURATION.USE_WEBHOOK:
            run_webhook()
        else:
            asyncio.run(run_polling())
    except (KeyboardInterrupt, SystemExit, RuntimeError):
        pass


if __name__ == "__main__":
    start_bot()
