import logging
from src.config import CONFIGURATION


if CONFIGURATION.IS_DEVELOPMENT:
    logging.basicConfig(
        format="%(levelname)-s [%(asctime)s] - %(name)s - %(message)s",
        level=CONFIGURATION.LOGGER.level,
    )
else:
    logging.basicConfig(
        format="%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s",
        encoding="utf-8",
        filename=CONFIGURATION.LOGGER.log_path,
        level=CONFIGURATION.LOGGER.level,
    )
