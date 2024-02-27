from sqlalchemy.ext.asyncio import AsyncSession


class TopicRepo:
    """Implements repository for topic entity"""

    def __init__(self, session: AsyncSession):
        self._session = session
