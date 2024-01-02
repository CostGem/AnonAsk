from aiogram import Bot, Dispatcher
from termcolor import cprint


async def on_startup(dispatcher: Dispatcher, bot: Bot) -> None:
    """Bot startup"""

    cprint("Bot started", "green")


async def on_shutdown(dispatcher: Dispatcher, bot: Bot) -> None:
    """Bot shutdown"""

    await bot.session.close()
    await dispatcher.storage.close()

    cprint("Bot stopped", "red")
