from typing import AsyncContextManager, Callable, Optional

from aiogram.utils.formatting import Url
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine

from src.database.models.base import BaseModel


async def create_session_pool(
    url: str, echo: bool = True
) -> Callable[[], AsyncContextManager[AsyncSession]]:
    """
    The `create_session_pool` function creates a session pool for an async SQLAlchemy database
    connection.

    :param db: The `db` parameter is a string that represents the database URL or connection string. It
    is used to connect to the database
    :type db: str
    :param echo: The `echo` parameter is a boolean flag that determines whether or not the engine should
    log all SQL statements that are executed. If `echo` is set to `True`, the engine will log the
    statements, and if it is set to `False`, the engine will not log the statements, defaults to True
    :type echo: bool (optional)
    :return: The function `create_session_pool` returns a callable object that, when called, returns an
    asynchronous context manager that yields an `AsyncSession` object.
    """
    engine: AsyncEngine = create_async_engine(
        url=url, echo=echo, future=True, _is_async=True
    )

    async with engine.begin() as connection:
        await connection.run_sync(BaseModel.metadata.create_all)

    session_pool = async_sessionmaker(bind=engine, expire_on_commit=False)

    return session_pool


class SessionMakerManager:
    """
    The `SessionMakerManager` class is a singleton implementation that manages a session pool for a
    database connection.
    """

    __session_pool: Optional[Callable[[], AsyncContextManager[AsyncSession]]] = None

    def __new__(cls):
        """
        The function is a singleton implementation that ensures only one instance of the class is created.

        :param cls: The `cls` parameter in this code refers to the class itself. It is a convention to use
        `cls` instead of `self` when defining class methods or static methods. In this case, `cls` is used
        to refer to the `SessionMakerManager` class
        :return: The `__new__` method is returning the `cls.instance` attribute.
        """
        if not hasattr(cls, "instance"):
            cls.instance = super(SessionMakerManager, cls).__new__(cls)

        return cls.instance

    async def __init_pool(self, url: str, echo: bool = False) -> None:
        """
        The function initializes a session pool for a database connection.

        :param db: The `db` parameter is a string that represents the path to the database file. It is used
        to specify the location of the database that the session pool will connect to
        :type db: str
        :param echo: The `echo` parameter is a boolean flag that determines whether or not the database
        engine should log all SQL statements that are executed. If `echo` is set to `True`, the engine will
        log all SQL statements to the console. If `echo` is set to `False`, no logging will, defaults to
        False
        :type echo: bool (optional)
        """
        if not self.__session_pool:
            self.__session_pool = await create_session_pool(url=url, echo=echo)

    async def get_pool(self) -> Callable[[], AsyncContextManager[AsyncSession]]:
        """
        The function `get_pool` returns a callable that returns an asynchronous context manager for an async
        session pool.
        :return: The `get_pool` method returns a callable object that takes no arguments and returns an
        asynchronous context manager that yields an `AsyncSession` object.
        """
        await self.__init_pool()
        return self.__session_pool


session_manager: SessionMakerManager = SessionMakerManager()
