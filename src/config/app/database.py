import environ
from sqlalchemy import URL


@environ.config(prefix="POSTGRES")
class DatabaseConfig:
    HOST: str = environ.var()
    DB: str = environ.var()
    USER: str = environ.var()
    PASSWORD: str = environ.var()
    PORT: int = environ.var(converter=int, default=5432)

    POOL_SIZE: int = environ.var(default=10, converter=int)
    ECHO_MODE: bool = environ.bool_var(default=True)

    @property
    def connection_url(self) -> str:
        """Returns database connection url"""

        return URL.create(
            drivername="postgresql+asyncpg",
            username=self.USER,
            database=self.DB,
            password=self.PASSWORD,
            port=self.PORT,
            host=self.HOST,
        ).render_as_string(hide_password=False)
