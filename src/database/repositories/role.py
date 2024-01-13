from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import RoleModel
from src.database.repositories.base import BaseRepository


class RoleRepository(BaseRepository[RoleModel]):
    """Role repository"""

    def __init__(self, session: AsyncSession):
        """Initialize role repository"""

        super().__init__(session=session)

    async def get(self, role_id: int) -> Optional[RoleModel]:
        """
        Return role by ID

        :param role_id: Role ID
        """

        return await self.session.scalar(
            select(RoleModel).where(RoleModel.id == role_id)
        )
