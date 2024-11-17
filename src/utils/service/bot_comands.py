from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeChat
from dependency_injector.wiring import Provide, inject

from src.containers.app import AppContainer
from src.translation.translator import LocalizedTranslator


@inject
async def set_bot_commands(
        translator: LocalizedTranslator,
        bot: Bot = Provide[AppContainer.bot],
) -> None:
    """
    Set the bot commands

    :param translator: Translator
    :param bot: Bot instance
    """

    await bot.set_my_commands(
        commands=[
            BotCommand(
                command="start",
                description=translator.get(key="start_command_description")
            )
        ],
        scope=BotCommandScopeChat(type="chat", chat_id=user_data.user.user_id),
        language_code=translator.locale
    )
