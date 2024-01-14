from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import LessonModel
from src.database.repositories.base import BaseRepository


class LessonRepository(BaseRepository[LessonModel]):
    """Lesson repository"""

    def __init__(self, session: AsyncSession):
        """Initialize lesson repository"""

        super().__init__(session=session)

    async def get_all_by_schedule_type(self, schedule_id: int) -> List[LessonModel]:
        """
        Return lessons by schedule ID

        :param schedule_id: Schedule ID
        """

        lessons = await self.session.scalars(
            select(LessonModel).where(LessonModel.schedule_id == schedule_id).order_by(LessonModel.id)
        )

        return lessons.all()
