from dataclasses import dataclass
from os import getenv
from typing import Optional

from dotenv import find_dotenv, load_dotenv

from src.config.bot import BotConfiguration
from src.config.database import DatabaseConfiguration
from src.config.logger import LoggerConfiguration
from src.config.redis import RedisConfiguration


@dataclass
class Config:
    IS_DOCKER: bool = False
    USE_WEBHOOK: bool = False
    IS_DEVELOPMENT: bool = True
    BOT: Optional[BotConfiguration] = None
    DATABASE: Optional[DatabaseConfiguration] = None
    REDIS: Optional[RedisConfiguration] = None
    LOGGER: Optional[LoggerConfiguration] = None

    def __init__(self) -> None:
        self.load_env_files()
        self.load_from_env()

    def load_env_files(self) -> None:
        """Load env files"""

        self.IS_DOCKER = bool(getenv("IS_DOCKER"))

        if self.IS_DOCKER:
            special_dotenv_path: str = find_dotenv(filename=".env.docker")
        else:
            special_dotenv_path: str = find_dotenv(filename=".env.local")

        load_dotenv(dotenv_path=special_dotenv_path)

    def load_from_env(self) -> None:
        """Load data from env file"""

        self.USE_WEBHOOK = getenv("USE_WEBHOOK") == "true"
        self.IS_DEVELOPMENT = True
        self.BOT = BotConfiguration()
        self.DATABASE = DatabaseConfiguration()
        self.REDIS = RedisConfiguration()
        self.LOGGER = LoggerConfiguration(is_dev=self.IS_DEVELOPMENT)
