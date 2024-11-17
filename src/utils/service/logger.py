import logging
import sys


def configure_logging() -> None:
    """Configures logging for the application"""

    logging.basicConfig(
        level=logging.INFO,
        stream=sys.stdout,
        format="[%(levelname)s] %(asctime)s - %(name)s - %(message)s",
        datefmt="%d.%m.%Y %H:%M:%S"
    )
