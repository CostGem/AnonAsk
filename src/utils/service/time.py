from datetime import datetime, UTC


def utcnow() -> datetime:
    """Returns current UTC datetime"""

    return datetime.now(UTC)
