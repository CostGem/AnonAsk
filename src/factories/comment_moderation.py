from aiogram.filters.callback_data import CallbackData


class CommentDeleteFactory(CallbackData, prefix="comment_delete"):
    comment_id: int


class CommentUserBanFactory(CallbackData, prefix="comment_user_block"):
    comment_id: int
