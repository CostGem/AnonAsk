from typing import Optional

from sqlalchemy import select, update
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

    async def update_post_message_id_in_chat(self, post_id: int, post_message_id: int) -> None:
        """
        Update post id in chat

        :param post_id: Post ID
        :param post_message_id: Post message ID
        """

        await self.session.execute(
            update(PostModel).where(PostModel.id == post_id).values(post_id_in_chat=post_message_id)
        )

        await self.session.commit()

    async def create(self, post_id: int, is_commentable: bool) -> PostModel:
        """
        Create a new post

        :param post_id: Post id
        :param is_commentable: Post is commentable
        """

        self.session.add(
            instance=PostModel(
                id=post_id,
                is_commentable=is_commentable
            )
        )
        await self.session.commit()

        return await self.session.scalar(
            select(
                PostModel
            ).where(
                PostModel.id == post_id
            )
        )
