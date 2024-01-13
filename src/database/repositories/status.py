from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import StatusModel, UserStatusModel
from src.database.repositories.base import BaseRepository


class StatusRepository(BaseRepository[StatusModel]):
    """Status repository"""

    def __init__(self, session: AsyncSession):
        """Initialize status repository"""

        super().__init__(session=session)

    async def get(self, status_id: int) -> Optional[StatusModel]:
        """
        Return status by ID

        :param status_id: Role ID
        """

        return await self.session.scalar(
            select(StatusModel).where(StatusModel.id == status_id)
        )

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
