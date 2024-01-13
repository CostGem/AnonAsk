from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import RoleModel, PostModel, CommentModel
from src.database.repositories.base import BaseRepository


class CommentRepository(BaseRepository[CommentModel]):
    """Comment repository"""

    def __init__(self, session: AsyncSession):
        """Initialize comment repository"""

        super().__init__(session=session)

    async def get(self, comment_id: int) -> Optional[CommentModel]:
        """
        Return comment by ID

        :param comment_id: Comment ID
        """

        return await self.session.scalar(
            select(CommentModel).where(CommentModel.id == comment_id)
        )
