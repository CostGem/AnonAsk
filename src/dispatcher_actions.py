from aiogram import Bot, Dispatcher
from apscheduler.schedulers.asyncio import AsyncIOScheduler


async def on_startup(dispatcher: Dispatcher) -> None:
    """Bot startup"""

    scheduler: AsyncIOScheduler = dispatcher["scheduler"]

    scheduler.start()


async def on_shutdown(dispatcher: Dispatcher, bot: Bot) -> None:
    """Bot shutdown"""

    await bot.session.close()
    await dispatcher.storage.close()
