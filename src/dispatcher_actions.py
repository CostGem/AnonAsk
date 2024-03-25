from aiogram import Bot, Dispatcher
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from termcolor import cprint

from src.middlewares import register_middlewares


async def on_startup(dispatcher: Dispatcher) -> None:
    """Bot startup"""

    register_middlewares(dp=dispatcher)

    scheduler: AsyncIOScheduler = dispatcher["scheduler"]

    scheduler.start()

    cprint("Bot started", "green")


async def on_shutdown(dispatcher: Dispatcher, bot: Bot) -> None:
    """Bot shutdown"""

    await bot.session.close()
    await dispatcher.storage.close()

    cprint("Bot stopped", "red")
