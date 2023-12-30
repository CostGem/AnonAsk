from enum import StrEnum


class DatabaseType(StrEnum):
    MARIADB: str = "mariadb"
    MICROSOFT: str = "mssql"
    MYSQL: str = "mysql"
    ORACLE: str = "oracle"
    POSTGRESQL: str = "postgresql"
    SQLITE: str = "sqlite"


class DatabaseDriver(StrEnum):
    # MariaDB
    MARIADB_CONNECTOR: str = "mariadbconnector"

    # Microsoft
    AIOODBC: str = "aioodbc"
    PYMSSQL: str = "pymssql"

    # MySql
    AIOMYSQL: str = "aiomysql"
    ASYNCMY: str = "asyncmy"
    CYMYSQL: str = "cymysql"
    MYSQL_CONNECTOR: str = "mysqlconnector"
    MYSQLDB: str = "mysqldb"
    PYMYSQL: str = "pymysql"
    PYODBC: str = "pyodbc"

    # Oracle
    CX_ORACLE: str = "cx_oracle"
    ORACLEDB: str = "oracledb"

    # Postgresql
    ASYNCPG: str = "asyncpg"
    PG8000: str = "pg8000"
    PSYCOPG: str = "psycopg"
    PSYCOPG2: str = "psycopg2"
    PSYCOPG2CFFI: str = "psycopg2cffi"

    # Sqlite
    AIOSQLITE: str = "aiosqlite"
    PYSQLCIPHER: str = "pysqlcipher"
    PYSQLITE: str = "pysqlite"
