from src.enums import DatabaseDriver, DatabaseType


class DatabaseDriverError(Exception):
    """Incorrect database driver error"""

    def __init__(self, database: DatabaseType, driver: DatabaseDriver) -> None:
        super().__init__(f"Driver {driver} for database {database} is selected incorrectly")
