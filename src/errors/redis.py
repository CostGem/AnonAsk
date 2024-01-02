class InvalidRedisKeyError(Exception):
    def __init__(self, key: str) -> None:
        super().__init__(f"Invalid redis key: {key}")
