from typing import Callable, Dict, Any, Awaitable, Optional

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from sqlalchemy.ext.asyncio import AsyncSession

from src.classes.user.user_data import UserData
from src.database.models import UserModel, RoleModel, StatusModel, LocaleModel
from src.database.repositories import UserRepository, RoleRepository, StatusRepository, LocaleRepository


class UserAccountMiddleware(BaseMiddleware):
    """User account middleware"""

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any],
    ) -> Any:
        session: AsyncSession = data["session"]
        user_repository: UserRepository = UserRepository(session=session)
        role_repository: RoleRepository = RoleRepository(session=session)
        status_repository: StatusRepository = StatusRepository(session=session)
        locale_repository: LocaleRepository = LocaleRepository(session=session)

        user: Optional[UserModel] = await user_repository.get(user_id=event.from_user.id)
        role: Optional[RoleModel] = await role_repository.get(role_id=user.role_id) if user else None
        status: Optional[StatusModel] = await status_repository.get(status_id=user.status_id) if user else None
        locale: Optional[LocaleModel] = await locale_repository.get_user_locale(user=user) if user else None

        data["user_data"] = UserData(
            repository=user_repository,
            user=user,
            role=role,
            status=status,
            locale=locale
        )

        return await handler(event, data)
