from dataclasses import dataclass
from os import getenv

from src.config.bot import BotConfiguration
from src.config.database import DatabaseConfiguration
from src.config.env import IS_DOCKER
from src.config.logger import LoggerConfiguration
from src.config.redis import RedisConfiguration


class Config:
    USE_WEBHOOK: bool = getenv("USE_WEBHOOK") == "true"
    IS_DEVELOPMENT: bool = not IS_DOCKER
    BOT: BotConfiguration = BotConfiguration()
    DATABASE: DatabaseConfiguration = DatabaseConfiguration()
    REDIS: RedisConfiguration = RedisConfiguration()
    LOGGER: LoggerConfiguration = LoggerConfiguration(IS_DEVELOPMENT=IS_DEVELOPMENT)
