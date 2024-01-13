from typing import Optional, List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import AchievementModel, UserModel, UserAchievementModel
from src.database.repositories.base import BaseRepository


class AchievementRepository(BaseRepository[AchievementModel]):
    """Achievement repository"""

    def __init__(self, session: AsyncSession):
        """Initialize achievement repository"""

        super().__init__(session=session)

    async def get(self, achievement_id: int) -> Optional[AchievementModel]:
        """
        Return achievement by ID

        :param achievement_id: Achievement ID
        """

        return await self.session.scalar(
            select(AchievementModel).where(AchievementModel.id == achievement_id)
        )

    async def get_user_achievements(self, user: UserModel) -> List[AchievementModel]:
        """
        Return list of user statuses

        :param user: User
        """

        stmt = (
            select(AchievementModel)
            .filter(
                AchievementModel.id.in_(
                    select(
                        UserAchievementModel.achievement_id
                    ).filter(
                        UserAchievementModel.user_id == user.id
                    ).order_by(
                        UserAchievementModel.received_at
                    )
                )
            ).order_by(
                AchievementModel.id
            )
        )

        result = await self.session.scalars(stmt)
        return result.all()
