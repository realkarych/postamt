from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.topic import Topic as DBTopic
from app.entities.topic import DecryptedTopic, EncryptedTopic
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from app.exceptions.repo import DBError, ModelExists
import logging

from app.services.cryptography.cryptographer import TopicCryptographer


class TopicRepo:
    """Implements repository for topic entity"""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def add_topic(self, topic: DecryptedTopic, update_when_exists: bool = False) -> None:
        """Adds topic to database"""
        async with self._session.begin():
            try:
                db_topic = _convert_topic_to_db_topic(topic.encrypt())
                if update_when_exists:
                    logging.info("Merging topic: %s", db_topic)
                    await self._session.merge(db_topic)
                else:
                    self._session.add(db_topic)
                await self._session.flush()

            except IntegrityError as e:
                await self._session.rollback()
                raise ModelExists("Failed to add topic to the database") from e
            except SQLAlchemyError as e:
                await self._session.rollback()
                raise DBError("Failed to add topic to the database") from e

    async def get_topic(self, crypto: TopicCryptographer, forum_id: int, topic_id: int) -> Optional[DecryptedTopic]:
        """Gets topic from the database"""
        try:
            query = select(DBTopic).where(DBTopic.forum_id == forum_id, DBTopic.topic_id == topic_id)
            result = await self._session.execute(query)
            db_topic = result.scalar_one_or_none()
            return _convert_db_topic_to_topic(crypto, db_topic).decrypt() if db_topic else None
        except SQLAlchemyError as e:
            raise DBError("Failed to get topic from the database") from e


def _convert_topic_to_db_topic(topic: EncryptedTopic) -> DBTopic:
    return DBTopic(forum_id=topic.forum_id, topic_id=topic.topic_id, topic_title=topic.topic_title)


def _convert_db_topic_to_topic(crypto: TopicCryptographer, db_topic: DBTopic) -> EncryptedTopic:
    return EncryptedTopic(
        _crypto=crypto,
        forum_id=int(str(db_topic.forum_id)),
        topic_id=int(str(db_topic.topic_id)),
        topic_title=bytes(db_topic.topic_title),  # type: ignore
    )
