from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeChat

from src.classes.user.user_data import UserData
from src.enums import Role
from src.translation.translator import LocalizedTranslator


async def set_bot_commands(user_data: UserData, bot: Bot, translator: LocalizedTranslator) -> None:
    """
    Set the bot commands for users and admins

    :param user_data: User data
    :param bot: Bot
    :param translator: Translator
    """

    if user_data.role.level == Role.ADMIN:
        await bot.set_my_commands(
            commands=[
                BotCommand(
                    command="start",
                    description=translator.get(key="start_command_description")
                ),
                BotCommand(
                    command="timetable",
                    description=translator.get(key="timetable_command_description")
                )
            ],
            scope=BotCommandScopeChat(type="chat", chat_id=user_data.user.user_id),
            language_code=translator.locale
        )
    else:
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
