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
