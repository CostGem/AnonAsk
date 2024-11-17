import os
from os import getenv

import environ
from dotenv import dotenv_values, find_dotenv

from src.config.config import AppConfig

IS_DOCKER: bool = bool(getenv("IS_DOCKER", False))

CONFIGURATION: AppConfig = environ.to_config(
    AppConfig,
    environ=os.environ if IS_DOCKER else dotenv_values(
        dotenv_path=find_dotenv(
            filename=".env.local"
        )
    ),
)

__all__ = [CONFIGURATION]
