import environ

from src.config.app.bot import BotConfig
from src.config.app.database import DatabaseConfig
from src.config.app.redis import RedisConfig


@environ.config(prefix="")
class AppConfig:
    IS_DOCKER: bool = environ.bool_var(default=False)
    IS_DEVELOPMENT: bool = environ.bool_var(default=False)

    DATABASE: DatabaseConfig = environ.group(DatabaseConfig)
    BOT: BotConfig = environ.group(BotConfig)
    REDIS: RedisConfig = environ.group(RedisConfig)
