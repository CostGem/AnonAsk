from datetime import date
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import TimetableModel
from src.database.repositories.base import BaseRepository


class TimetableRepository(BaseRepository[TimetableModel]):
    """Timetable repository"""

    def __init__(self, session: AsyncSession):
        """Initialize timetable repository"""

        super().__init__(session=session)

    async def get_by_date(self, timetable_date: date) -> Optional[TimetableModel]:
        """
        Return timetable by date

        :param timetable_date: Timetable date
        """

        return await self.session.scalar(
            select(TimetableModel).where(TimetableModel.date == timetable_date)
        )

    async def exists(self, timetable_date: date) -> Optional[TimetableModel]:
        """
        Return timetable exists by date

        :param timetable_date: Timetable date
        """

        query = select(select(TimetableModel).where(TimetableModel.date == timetable_date).exists())

        return await self.session.scalar(query)

    async def create(self, timetable_date: date, photo: str, schedule_id: int) -> None:
        """
        Create timetable

        :param timetable_date: Timetable date
        :param photo: Photo of timetable
        :param schedule_id: Timetable schedule type ID
        """

        self.session.add(
            instance=TimetableModel(
                schedule_id=schedule_id,
                photo=photo,
                date=timetable_date
            )
        )

        await self.session.commit()
