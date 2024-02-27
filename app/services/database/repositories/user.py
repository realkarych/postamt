from sqlalchemy.ext.asyncio import AsyncSession


class UserRepo:
    """Implements repository for user entity"""

    def __init__(self, session: AsyncSession):
        self._session = session
