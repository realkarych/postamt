from sqlalchemy.ext.asyncio import AsyncSession


class ForumRepository:
    """Implements ORM for forum entity"""

    def __init__(self, session: AsyncSession):
        self._session = session
