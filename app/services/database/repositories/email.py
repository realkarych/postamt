from sqlalchemy.ext.asyncio import AsyncSession


class EmailRepo:
    """Implements repository for email entity"""

    def __init__(self, session: AsyncSession):
        self._session = session
