from sqlalchemy import Column, BigInteger, Boolean, String
from app.services.database.base import BASE


class EmailBox(BASE):
    """Implements model for email boxes"""

    __tablename__ = "email_boxes"

    id = Column(BigInteger, primary_key=True, unique=True, autoincrement=True)
    owner_id = Column(BigInteger, nullable=False)
    forum_id = Column(BigInteger, nullable=False)
    last_handled_email_id = Column(BigInteger, nullable=False, default=0)
    is_active = Column(Boolean, default=True)


class EmailAuthData(BASE):
    """Implements model for email auth datas"""

    __tablename__ = "email_auth_datas"

    emailbox_id = Column(BigInteger, primary_key=True, nullable=False)
    email_server_id = Column(String, nullable=False)
    email_address = Column(String, nullable=False)
    email_password = Column(String, nullable=False)


class Topic(BASE):
    """Implements model for topics"""

    __tablename__ = "topics"

    forum_id = Column(BigInteger, primary_key=True, nullable=False)
    topic_id = Column(BigInteger, nullable=False)
    topic_title = Column(String, nullable=False)
