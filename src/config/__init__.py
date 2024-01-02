from dataclasses import dataclass
from src.config.bot import BotConfiguration
from src.config.database import DatabaseConfiguration

from src.config.env import IS_DOCKER
from src.config.logger import LoggerConfiguration
from src.config.redis import RedisConfiguration


@dataclass
class Config:
    IS_DEVELOPMENT: bool = not IS_DOCKER
    BOT: BotConfiguration = BotConfiguration()
    DATABASE: DatabaseConfiguration = DatabaseConfiguration()
    REDIS: RedisConfiguration = RedisConfiguration()
    LOGGER: LoggerConfiguration = LoggerConfiguration(IS_DEVELOPMENT=IS_DEVELOPMENT)

CONFIGURATION = Config()
