from typing import Optional

from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine

from src.database.models.base import BaseModel


async def create_session_pool(url: str, echo: bool = True) -> async_sessionmaker:
    """
    Create a session pool for an async SQLAlchemy database connection

    :param url: Url
    :param echo: Enable SQLAlchemy's echo mode for debugging
    """

    engine: AsyncEngine = create_async_engine(
        url=url, echo=echo, future=True, _is_async=True
    )

    async with engine.begin() as connection:
        await connection.run_sync(BaseModel.metadata.create_all)

    session_pool = async_sessionmaker(bind=engine, expire_on_commit=False)

    return session_pool


class SessionMakerManager:
    """Singleton implementation that manages a session pool for a database connection"""

    __session_pool: Optional[async_sessionmaker] = None

    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(SessionMakerManager, cls).__new__(cls)

        return cls.instance

    async def __init_pool(self, url: str, echo: bool = False) -> None:
        """
        The function initializes a session pool for a database connection

        :param url: The database connection URL
        :param echo: Enable SQLAlchemy's echo mode for debugging
        """

        if not self.__session_pool:
            self.__session_pool = await create_session_pool(url=url, echo=echo)

    async def get_pool(self, url: str) -> async_sessionmaker:
        """
        Returns a callable that returns an asynchronous context manager for an async session pool

        :param url: The database connection URL
        """

        await self.__init_pool(url=url)
        return self.__session_pool
