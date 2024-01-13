from os import getenv

from pydantic import BaseModel
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


class DatabaseConfiguration(BaseModel):
    host: str = getenv("POSTGRES_HOST")
    username: str = getenv("POSTGRES_USER")
    password: str = getenv("POSTGRES_PASSWORD")
    name: str = getenv("POSTGRES_DB")
    port: int = int(getenv("POSTGRES_PORT", 5432))

    database: DatabaseType = DatabaseType.POSTGRESQL
    driver: DatabaseDriver = DatabaseDriver.ASYNCPG

    pool_size: int = 10
    echo_mode: bool = True

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
