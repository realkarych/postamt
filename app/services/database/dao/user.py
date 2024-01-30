from sqlalchemy.ext.asyncio import AsyncSession

from app.entities.user import User


class UserRepository:
    """ORM queries for users table"""

    def __init__(self, session: AsyncSession):
        self._session = session

    async def add_user(self, user: User) -> None:
        await self._session.merge(user.to_db_model())

    async def commit(self):
        await self._session.commit()
