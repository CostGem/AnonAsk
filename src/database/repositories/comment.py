from typing import Optional, List

from sqlalchemy import select, desc, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import CommentModel, UserModel, PostModel
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

    async def get_child_comments(self, parent_comment_id: int) -> List[CommentModel]:
        """
        Return child comments by parent comment ID

        :param parent_comment_id: Parent comment ID
        """

        comments = await self.session.scalars(
            select(CommentModel).where(CommentModel.parent_comment_id == parent_comment_id)
        )

        return comments.all()

    async def get_last_comment(self, user: UserModel) -> Optional[CommentModel]:
        """
        Return last user comment

        :param user: User
        """

        return await self.session.scalar(
            select(
                CommentModel
            ).where(
                CommentModel.user_id == user.id
            ).order_by(
                desc(CommentModel.commented_at)
            )
        )

    async def create(self, user: UserModel, post: PostModel, parent_comment_id: Optional[int] = None) -> CommentModel:
        """
        Create a new comment

        :param user: User
        :param post: Post in channel
        :param parent_comment_id: Parent comment ID
        """

        self.session.add(
            instance=CommentModel(
                user_id=user.id,
                post_id=post.id,
                parent_comment_id=parent_comment_id
            )
        )

        await self.session.commit()

        return await self.session.scalar(
            select(
                CommentModel
            ).where(
                CommentModel.post_id == post.id,
                CommentModel.user_id == user.user_id
            )
        )

    async def update_comment_message_id(self, comment: CommentModel, message_id: int) -> None:
        """
        Update comment message ID

        :param comment: Comment
        :param message_id: Message ID
        """

        await self.session.execute(
            update(
                CommentModel
            ).where(
                CommentModel.id == comment.id
            ).values(
                message_id=message_id
            )
        )

        await self.session.commit()
