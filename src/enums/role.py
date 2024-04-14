from enum import IntEnum


class Role(IntEnum):
    USER: int = 1
    SCHEDULE_MANAGER: int = 2
    EDITOR: int = 3
    ADMIN: int = 4
