from typing import Optional, List

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import StatusModel, UserStatusModel, UserModel
from src.database.repositories.base import BaseRepository


class StatusRepository(BaseRepository[StatusModel]):
    """Status repository"""

    def __init__(self, session: AsyncSession):
        """Initialize status repository"""

        super().__init__(session=session)

    async def get(self, status_id: int) -> Optional[StatusModel]:
        """
        Return status by ID

        :param status_id: Status ID
        """

        return await self.session.scalar(
            select(StatusModel).where(StatusModel.id == status_id)
        )

    async def user_has_status(self, user_id: int, status_id: int) -> bool:
        """
        Return True if user has status, else False

        :param user_id: User ID
        :param status_id: Status ID
        """

        query = select(
            select(
                UserStatusModel
            ).where(
                UserStatusModel.user_id == user_id,
                UserStatusModel.status_id == status_id
            ).exists()
        )

        return await self.session.scalar(query)

    async def give_default_statuses_to_user(self, user_id: int) -> None:
        """
        Give to user default statuses

        :param user_id: User ID
        """

        self.session.add_all(
            instances=[
                UserStatusModel(
                    user_id=user_id,
                    status_id=1
                ),
                UserStatusModel(
                    user_id=user_id,
                    status_id=2
                )
            ]
        )

        await self.session.commit()

    async def get_user_statuses(self, user: UserModel) -> List[StatusModel]:
        """
        Return list of user statuses

        :param user: User
        """

        stmt = (
            select(StatusModel)
            .filter(
                StatusModel.id.in_(
                    select(
                        UserStatusModel.status_id
                    ).filter(
                        UserStatusModel.user_id == user.id
                    ).order_by(
                        UserStatusModel.received_at
                    )
                )
            ).order_by(
                StatusModel.id
            )
        )

        result = await self.session.scalars(stmt)
        return result.all()

    async def update_user_status(self, user: UserModel, status_id: int) -> None:
        """
        Update user status

        :param user: User
        :param status_id: Status ID
        """

        await self.session.execute(
            update(
                table=UserModel
            ).where(
                UserModel.id == user.id
            ).values(
                status_id=status_id
            )
        )

        await self.session.commit()
