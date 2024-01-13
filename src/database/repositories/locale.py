from typing import Optional, List

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import LocaleModel, UserModel
from src.database.repositories.base import BaseRepository
from src.enums import Locale


class LocaleRepository(BaseRepository[LocaleModel]):
    """Locale repository"""

    def __init__(self, session: AsyncSession):
        """Initialize locale repository"""

        super().__init__(session=session)

    async def get_by_code(self, locale_code: str) -> Optional[LocaleModel]:
        """
        Return locale by code

        :param locale_code: Locale code
        """

        return await self.session.scalar(
            select(LocaleModel).where(LocaleModel.code == locale_code)
        )

    async def get_by_id(self, locale_id: int) -> Optional[LocaleModel]:
        """
        Return locale by id

        :param locale_id: Locale id
        """

        return await self.session.scalar(
            select(LocaleModel).where(LocaleModel.id == locale_id)
        )

    async def get_user_locale(self, user: UserModel) -> LocaleModel:
        """
        Return user locale

        :param user: User
        """

        if user.locale_id:
            locale = await self.get_by_id(locale_id=user.locale_id)
        else:
            locale = await self.get_by_code(locale_code=Locale.RU)

            await self.update_user_locale(user=user, locale_id=locale.id)

        return locale

    async def get_all(self) -> List[LocaleModel]:
        """
        Return all locales
        """

        locales = await self.session.scalars(
            select(LocaleModel)
        )

        return locales.all()

    async def update_user_locale(self, user: UserModel, locale_id: int) -> None:
        """
        Update user locale

        :param user: User:
        :param locale_id: Locale ID
        """

        await self.session.execute(
            update(
                table=UserModel
            ).where(
                UserModel.id == user.id
            ).values(
                locale_id=locale_id
            )
        )

        await self.session.commit()
