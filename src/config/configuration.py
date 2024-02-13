from dataclasses import dataclass
from os import getenv
from typing import Self

from src.config.bot import BotConfiguration
from src.config.database import DatabaseConfiguration
from src.config.logger import LoggerConfiguration
from src.config.redis import RedisConfiguration


@dataclass
class Config:
    USE_WEBHOOK: bool
    IS_DEVELOPMENT: bool
    BOT: BotConfiguration
    DATABASE: DatabaseConfiguration
    REDIS: RedisConfiguration
    LOGGER: LoggerConfiguration

    def load(self) -> Self:
        self.USE_WEBHOOK = getenv("USE_WEBHOOK") == "true"
        self.IS_DEVELOPMENT = True
        self.BOT = BotConfiguration()
        self.DATABASE = DatabaseConfiguration()
        self.REDIS = RedisConfiguration()
        self.LOGGER = LoggerConfiguration(is_dev=self.IS_DEVELOPMENT)

        return self
