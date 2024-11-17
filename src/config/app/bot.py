import environ
from aiogram.enums import ParseMode


@environ.config(prefix="BOT")
class BotConfig:
    TOKEN: str = environ.var()

    PARSE_MODE: ParseMode = ParseMode.HTML
    DISABLE_WEB_PAGE_PREVIEW: bool = True
    PROTECT_CONTENT: bool = False
