from typing import Optional, List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import ScheduleTypeModel
from src.database.repositories.base import BaseRepository


class ScheduleRepository(BaseRepository[ScheduleTypeModel]):
    """Schedule repository"""

    def __init__(self, session: AsyncSession):
        """Initialize schedule repository"""

        super().__init__(session=session)

    async def get(self, schedule_id: int) -> Optional[ScheduleTypeModel]:
        """
        Return schedule by ID

        :param schedule_id: Schedule ID
        """

        return await self.session.scalar(
            select(ScheduleTypeModel).where(ScheduleTypeModel.id == schedule_id)
        )

    async def get_all(self) -> List[ScheduleTypeModel]:
        """
        Return all schedule types
        """

        result = await self.session.scalars(
            select(ScheduleTypeModel).order_by(ScheduleTypeModel.id)
        )
        return result.all()
