from aiogram.types import BotCommand, Bot

from src.translation.translator import LocalizedTranslator


async def set_bot_commands(bot: Bot, translator: LocalizedTranslator) -> None:
    """Set the bot commands"""

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
