from typing import Optional, Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import UserModel, LocaleModel
from src.database.repositories.base import BaseRepository


class LocaleRepository(BaseRepository[LocaleModel]):
    """Locale repository"""

    def __init__(self, session: AsyncSession):
        """Initialize user repository"""

        super().__init__(session=session)

    async def get_by_pk(self, locale_id: int) -> Optional[LocaleModel]:
        """
        Return locale by pk

        :param locale_id: Locale pk
        """

        return await self.session.scalar(
            select(LocaleModel).where(LocaleModel.id == locale_id)
        )

    async def get_by_code(self, locale_code: str) -> Optional[LocaleModel]:
        """
        Return locale by locale code

        :param locale_code: Locale code
        """

        return await self.session.scalar(
            select(LocaleModel).where(LocaleModel.code == locale_code)
        )

    async def get_all(self, user: UserModel) -> Sequence[LocaleModel]:
        """Return all locales"""

        if user.locale_id:
            locales = await self.session.scalars(
                select(LocaleModel).where(LocaleModel.id.not_in(other=[user.locale_id]))
            )
        else:
            locales = await self.session.scalars(select(LocaleModel))

        return locales.all()
