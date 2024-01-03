import logging
from typing import Union


class LoggerConfiguration:
    log_path: str = "logs/logs.log"
    level: Union[str, int] = logging.ERROR

    def __init__(self, is_dev: bool = False) -> None:
        if is_dev:
            self.level = logging.DEBUG
