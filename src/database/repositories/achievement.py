from typing import Optional, List

from sqlalchemy import select, func, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import AchievementModel, UserModel, UserAchievementModel, AchievementActivationCodeModel, \
    UserAchievementActivationModel, StatusModel, UserStatusModel
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

    async def get_achievement_activation_code(self, code: str) -> Optional[AchievementActivationCodeModel]:
        """
        Returns achievement activation code

        :param code: Achievement activation code
        """

        return await self.session.scalar(
            select(AchievementActivationCodeModel).where(AchievementActivationCodeModel.code == code)
        )

    async def user_has_achievement(self, user: UserModel, achievement_id: int) -> bool:
        """
        Returns True if user has achievement, else False

        :param user: User
        :param achievement_id: Achievement ID
        """

        query = select(
            select(
                UserAchievementModel
            ).where(
                UserAchievementModel.user_id == user.id,
                UserAchievementModel.achievement_id == achievement_id
            ).exists()
        )

        return await self.session.scalar(query)

    async def user_activated_achievement(self, user_id: int, activation_code_id: int) -> bool:
        """
        Returns True if user activated achievement, else False

        :param user_id: User ID
        :param activation_code_id: Achievement ID
        """

        query = select(
            select(
                UserAchievementActivationModel
            ).where(
                UserAchievementActivationModel.user_id == user_id,
                UserAchievementActivationModel.activation_code_id == activation_code_id
            ).exists()
        )

        return await self.session.scalar(query)

    async def activate_achievement(
            self,
            user: UserModel,
            achievement: AchievementModel,
            achievement_activation_code: AchievementActivationCodeModel,
            user_has_status: bool,
            status: StatusModel
    ) -> None:
        """
        Activate achievement

        :param user: User
        :param achievement: Achievement
        :param achievement_activation_code: AchievementActivationCode
        :param user_has_status: User has status
        :param status: Status
        """

        if not user_has_status:
            self.session.add(
                UserStatusModel(
                    user_id=user.id,
                    status_id=status.id
                )
            )

        self.session.add(
            instance=UserAchievementModel(
                user_id=user.id,
                achievement_id=achievement.id
            )
        )

        self.session.add(
            instance=UserAchievementActivationModel(
                user_id=user.id,
                activation_code_id=achievement_activation_code.id
            )
        )

        await self.session.commit()

        activation_count = await self.session.scalar(
            select(
                func.count(UserAchievementActivationModel)
            ).where(
                UserAchievementActivationModel.user_id == user.id,
                UserAchievementActivationModel.activation_code_id == achievement_activation_code.id
            )
        )

        if activation_count >= achievement_activation_code.activations_limit:
            await self.session.execute(
                delete(
                    UserAchievementActivationModel
                ).where(
                    UserAchievementActivationModel.activation_code_id == achievement_activation_code.id
                )
            )

            await self.session.execute(
                delete(
                    AchievementActivationCodeModel
                ).where(
                    AchievementActivationCodeModel.id == achievement_activation_code.id
                )
            )

            await self.session.commit()
