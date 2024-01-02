class InvalidTranslationKeyError(Exception):
    def __init__(self, key: str) -> None:
        super().__init__(f"Translation for key '{key}' not found")
