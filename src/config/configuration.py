from os import getenv

from config.bot import BotConfiguration
from config.database import DatabaseConfiguration
from config.logger import LoggerConfiguration
from config.redis import RedisConfiguration


class Config:
    USE_WEBHOOK: bool = getenv("USE_WEBHOOK") == "true"
    IS_DEVELOPMENT: bool = True
    BOT: BotConfiguration = BotConfiguration()
    DATABASE: DatabaseConfiguration = DatabaseConfiguration()
    REDIS: RedisConfiguration = RedisConfiguration()
    LOGGER: LoggerConfiguration = LoggerConfiguration(is_dev=IS_DEVELOPMENT)
