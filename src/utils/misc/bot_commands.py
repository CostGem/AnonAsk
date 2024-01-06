from typing import List

from aiogram import Bot
from aiogram.types import (
    BotCommand,
    BotCommandScopeDefault,
)
from src.translation.translator import LocalizedTranslator, TranslatorManager


async def set_localized_commands(bot: Bot, translator: LocalizedTranslator) -> None:
    """
    The function `set_localized_commands` sets the localized commands for a bot using the
    `set_my_commands` method.

    :param bot: The `bot` parameter is an instance of the `Bot` class, which represents your Telegram
    bot. It is used to interact with the Telegram Bot API and perform actions such as setting commands
    :type bot: Bot
    :param translator: The `translator` parameter is an instance of the `LocalizedTranslator` class. It
    is used for translating text to different languages based on the user's preferred language
    :type translator: LocalizedTranslator
    """

    commands: List[BotCommand] = [
        BotCommand(
            command="/start", description=translator.get(key="start_command_description")
        )
    ]

    await bot.set_my_commands(
        commands=commands,
        scope=BotCommandScopeDefault(),
        language_code=translator.locale
    )


async def set_bot_commands(bot: Bot):
    """
    The function sets basic private commands for a bot.

    :param bot: The "bot" parameter is an instance of the Bot class. It represents the Discord bot that
    you are using
    :type bot: Bot
    """

    for translator in TranslatorManager().translators.values():
        await set_localized_commands(bot=bot, translator=translator)
