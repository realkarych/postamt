from sqlalchemy.ext.asyncio import AsyncSession


class EmailRepository:
    """Implements ORM for email entity"""

    def __init__(self, session: AsyncSession):
        self._session = session
