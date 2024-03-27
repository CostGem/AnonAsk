from dataclasses import dataclass
from os import getenv
from typing import Optional

from sqlalchemy import URL

from src.enums import DatabaseDriver, DatabaseType
from src.errors.database import DatabaseDriverError

DATABASES_DRIVERS = {
    DatabaseType.MARIADB: (
        DatabaseDriver.MARIADB_CONNECTOR,
        DatabaseDriver.PYMYSQL
    ),
    DatabaseType.MICROSOFT: (
        DatabaseDriver.AIOODBC,
        DatabaseDriver.PYMSSQL,
        DatabaseDriver.PYODBC,
    ),
    DatabaseType.MYSQL: (
        DatabaseDriver.AIOMYSQL,
        DatabaseDriver.ASYNCMY,
        DatabaseDriver.CYMYSQL,
        DatabaseDriver.MYSQL_CONNECTOR,
        DatabaseDriver.MYSQLDB,
        DatabaseDriver.PYMYSQL,
        DatabaseDriver.PYODBC,
    ),
    DatabaseType.ORACLE: (
        DatabaseDriver.CX_ORACLE,
        DatabaseDriver.ORACLEDB,
    ),
    DatabaseType.POSTGRESQL: (
        DatabaseDriver.ASYNCPG,
        DatabaseDriver.PG8000,
        DatabaseDriver.PSYCOPG,
        DatabaseDriver.PSYCOPG2,
        DatabaseDriver.PSYCOPG2CFFI,
    ),
    DatabaseType.SQLITE: (
        DatabaseDriver.AIOSQLITE,
        DatabaseDriver.PYSQLCIPHER,
        DatabaseDriver.PYSQLITE,
    ),
}


@dataclass
class DatabaseConfiguration:
    host: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None
    name: Optional[str] = None
    port: int = 5432

    database: DatabaseType = DatabaseType.POSTGRESQL
    driver: DatabaseDriver = DatabaseDriver.ASYNCPG

    pool_size: int = 10
    echo_mode: bool = True

    def __init__(self) -> None:
        self.load_from_env()

    def load_from_env(self) -> None:
        """Load data from env file"""

        self.host = getenv("POSTGRES_HOST")
        self.username = getenv("POSTGRES_USER")
        self.password = getenv("POSTGRES_PASSWORD")
        self.name = getenv("POSTGRES_DB")
        self.port = int(getenv("POSTGRES_PORT", 5432))

    def build_connection_url(self) -> str:
        """Returns a database connection string"""

        if self.driver not in DATABASES_DRIVERS[self.database]:
            raise DatabaseDriverError(database=self.database, driver=self.driver)

        return URL.create(
            drivername=f"{self.database}+{self.driver}",
            username=self.username,
            database=self.name,
            password=self.password,
            port=self.port,
            host=self.host,
        ).render_as_string(hide_password=False)
