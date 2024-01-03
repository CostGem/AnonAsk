from aiogram import Bot, Dispatcher
from termcolor import cprint

from middlewares import register_middlewares
from utils.misc.bot_commands import set_bot_commands


async def on_startup(dispatcher: Dispatcher, bot: Bot) -> None:
    """Bot startup"""

    register_middlewares(dp=dispatcher)
    await set_bot_commands(bot=bot)

    cprint("Bot started", "green")


async def on_shutdown(dispatcher: Dispatcher, bot: Bot) -> None:
    """Bot shutdown"""

    await bot.session.close()
    await dispatcher.storage.close()

    cprint("Bot stopped", "red")
