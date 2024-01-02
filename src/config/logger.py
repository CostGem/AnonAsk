import logging
from dataclasses import dataclass
from typing import Union


@dataclass
class LoggerConfiguration:
    log_path: str = "logs/logs.log"
    level: Union[str, int] = logging.ERROR

    def __init__(self, is_development: bool = False) -> None:
        if is_development:
            self.level = logging.DEBUG
