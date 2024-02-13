import logging
from typing import Union

from pydantic import BaseModel


class LoggerConfiguration(BaseModel):
    log_path: str = "logs/logs.log"
    level: Union[str, int] = logging.ERROR

    def __init__(self, is_dev: bool = False) -> None:
        if is_dev:
            self.level = logging.DEBUG

            logging.basicConfig(
                format="%(levelname)-s [%(asctime)s] - %(name)s - %(message)s",
                level=self.level,
            )
        else:
            logging.basicConfig(
                format="%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s",
                encoding="utf-8",
                filename=self.log_path,
                level=self.level,
            )
