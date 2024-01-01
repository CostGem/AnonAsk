from typing import Optional

from aiogram.utils.formatting import Url
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine as _create_async_engine


async def create_async_engine(
        connection_url: Optional[Url, str],
        pool_size: int,
        echo_mode: bool
) -> AsyncEngine:
    """Creates an async SQLAlchemy engine"""

    return _create_async_engine(
        url=connection_url,
        pool_size=pool_size,
        echo=echo_mode
    )


async def async_session_maker(async_engine: AsyncEngine, expire_on_commit: bool) -> async_sessionmaker:
    """Creates an async SQLAlchemy session maker"""

    return async_sessionmaker(bind=async_engine, expire_on_commit=expire_on_commit)
