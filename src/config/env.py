import logging
from dataclasses import dataclass
from os import getenv
from typing import Optional, Union

from dotenv import load_dotenv, find_dotenv

from config.bot import BotConfiguration
from config.database import DatabaseConfiguration
from config.redis import RedisConfiguration

IS_DOCKER: Optional[str] = getenv("IS_DOCKER")

if IS_DOCKER:
    dotenv_path = find_dotenv(filename=".env.docker")
else:
    dotenv_path = find_dotenv(filename=".env.local")

load_dotenv(dotenv_path=dotenv_path)
