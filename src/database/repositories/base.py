import logging
from typing import Generic, TypeVar, Optional

from sqlalchemy.ext.asyncio import AsyncSession

AbstractModel = TypeVar("AbstractModel")


class BaseRepository(Generic[AbstractModel]):
    """Repository abstract class"""

    session: Optional[AsyncSession] = None

    def __init__(self, session: AsyncSession):
        """Initialize abstract repository class

        :param session: Session in which repository will work
        """

        self.session = session

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        try:
            await self.session.flush()
        except Exception as e:
            logging.error(msg=f"Error while flushing session: {e}", exc_info=True)
            await self.session.rollback()
        else:
            await self.session.commit()
