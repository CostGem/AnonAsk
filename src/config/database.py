from dataclasses import dataclass
from os import getenv
from typing import Optional

from sqlalchemy import URL

from enums.database import DatabaseDriver, DatabaseType
from errors.database import DatabaseDriverError

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
    host: Optional[str] = getenv("DATABASE_HOST")
    username: Optional[str] = getenv("DATABASE_USERNAME")
    password: Optional[str] = getenv("DATABASE_PASSWORD")
    name: Optional[str] = getenv("DATABASE_NAME")
    port: Optional[int] = int(getenv("DATABASE_PORT", 5432))

    database: Optional[DatabaseType] = DatabaseType.POSTGRESQL
    driver: Optional[DatabaseDriver] = DatabaseDriver.ASYNCPG

    def build_connection_url(self) -> str:
        """Returns a database connection string"""

        if self.database not in DATABASES_DRIVERS[self.database]:
            raise DatabaseDriverError(database=self.database, driver=self.driver)

        return URL.create(
            drivername=f"{self.database}+{self.driver}",
            username=self.username,
            database=self.name,
            password=self.password,
            port=self.port,
            host=self.host,
        ).render_as_string(hide_password=False)
