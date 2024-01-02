from dataclasses import dataclass
from os import getenv

from src.config.bot import BotConfiguration
from src.config.database import DatabaseConfiguration
from src.config.logger import LoggerConfiguration
from src.config.redis import RedisConfiguration


@dataclass
class Config:
    IS_DEVELOPMENT: bool = True
    USE_WEBHOOK: bool = bool(getenv("USE_WEBHOOK"))
    BOT: BotConfiguration = BotConfiguration()
    DATABASE: DatabaseConfiguration = DatabaseConfiguration()
    REDIS: RedisConfiguration = RedisConfiguration()
    LOGGER: LoggerConfiguration = LoggerConfiguration(is_development=IS_DEVELOPMENT)
