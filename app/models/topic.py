from sqlalchemy import Column, BigInteger, LargeBinary
from app.services.database.base import Base


class Topic(Base):
    """Implements model for topics"""

    __tablename__ = "topics"

    forum_id = Column(BigInteger, primary_key=True, nullable=False)
    topic_id = Column(BigInteger, nullable=False)
    topic_title = Column(LargeBinary, nullable=False)

    def __repr__(self) -> str:
        return f"Topic: {self.topic_title} | Topic ID: {self.topic_id} | Forum ID: {self.forum_id}"
