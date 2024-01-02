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
