from dataclasses import dataclass
import logging
from os import getenv
from typing import Optional, Union


class LoggerConfiguration:
    log_path: str = "logs/logs.log"
    level: Union[str, int] = logging.ERROR

    def __init__(self, IS_DEVELOPMENT: bool = False) -> None:
        if IS_DEVELOPMENT:
            self.level = logging.DEBUG
