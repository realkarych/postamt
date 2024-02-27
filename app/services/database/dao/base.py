from typing import TypeVar, Type, Generic

from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.services.database.base import Base

Model = TypeVar("Model", Base, Base)


class BaseDAO(Generic[Model]):
    """ORM queries for abstract table"""

    def __init__(self, model: Type[Model], session: AsyncSession):
        self._model = model
        self._session = session

    async def count(self) -> int:
        """Gets table size (number of rows)"""
        async with self._session.begin():
            result = await self._session.execute(select(func.count(self._model.id)))
            return int(result.scalar_one())
