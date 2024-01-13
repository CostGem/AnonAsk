from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import PostModel
from src.database.repositories.base import BaseRepository


class PostRepository(BaseRepository[PostModel]):
    """Post repository"""

    def __init__(self, session: AsyncSession):
        """Initialize post repository"""

        super().__init__(session=session)

    async def get(self, post_id: int) -> Optional[PostModel]:
        """
        Return post by ID

        :param post_id: Post ID
        """

        return await self.session.scalar(
            select(PostModel).where(PostModel.id == post_id)
        )
