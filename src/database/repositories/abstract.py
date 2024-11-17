import logging
from collections.abc import Sequence
from typing import Generic, Type, TypeVar, Union, Optional

from sqlalchemy import Select, delete, select, update, ColumnElement, Delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql._typing import _HasClauseElement
from sqlalchemy.sql.elements import SQLCoreOperations

from src.database.models.base import BaseModel

AbstractModel = TypeVar("AbstractModel")


class AbstractRepository(Generic[AbstractModel]):
    """Repository abstract class."""

    type_model: Type[BaseModel]
    session: AsyncSession

    def __init__(self, session: AsyncSession):
        """Initialize abstract repository class

        :param session: Session in which repository will work.
        """

        self.session = session

    async def get_by_ident(self, ident: Union[int, str]) -> Optional[AbstractModel]:
        """
        Get an ONE model from the database with PK.

        :param ident: Key which need to find entry in database
        """

        return await self.session.get(
            entity=self.type_model,
            ident=ident
        )

    async def get_by_where(
            self,
            *whereclause: Union[ColumnElement[bool], _HasClauseElement[bool], SQLCoreOperations[bool]]
    ) -> Optional[AbstractModel]:
        """
        Get an ONE model from the database with whereclause.


        :param whereclause: Clause by which entry will be found
        """

        statement: Select = select(self.type_model).where(*whereclause).limit(1)

        return await self.session.scalar(statement)

    async def get_many(
            self,
            whereclause: Union[ColumnElement[bool], _HasClauseElement[bool], SQLCoreOperations[bool]],
            limit: int = 100,
            order_by: Optional[ColumnElement] = None
    ) -> Sequence[BaseModel]:
        """
        Get many schemas from the database with whereclause.

        :param whereclause: Where clause for finding schemas
        :param limit: (Optional) Limit count of results
        :param order_by: (Optional) Order by clause.
        """

        statement: Select = select(self.type_model).where(whereclause).limit(limit)

        if order_by:
            statement = statement.order_by(order_by)

        return (await self.session.scalars(statement)).all()

    async def delete(
            self,
            whereclause: Union[ColumnElement[bool], _HasClauseElement[bool], SQLCoreOperations[bool]]
    ) -> None:
        """
        Delete model from the database.

        :param whereclause: Which statement
        :return: Nothing
        """

        statement: Delete = delete(self.type_model).where(whereclause)

        try:
            await self.session.execute(statement=statement)
            await self.session.flush()
        except Exception as ex:
            await self.session.rollback()
            logging.error(ex)
        else:
            await self.session.commit()

    async def update(
            self,
            whereclause: Union[ColumnElement[bool], _HasClauseElement[bool], SQLCoreOperations[bool]],
            **kwargs
    ) -> None:
        """Delete model from the database.

        :param whereclause: (Optional) Which statement
        :return: Nothing
        """

        try:
            await self.session.execute(
                statement=update(self.type_model).where(whereclause).values(**kwargs)
            )
            await self.session.flush()
        except Exception as ex:
            await self.session.rollback()
            logging.error(ex)
        else:
            await self.session.commit()

    # @abc.abstractmethod
    # async def new(self, *args, **kwargs) -> None:
    #     """Add new entry of model to the database."""
