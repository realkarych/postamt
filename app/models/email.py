from sqlalchemy import Column, BigInteger, Boolean, LargeBinary
from app.services.database.base import Base


class EmailBox(Base):
    """Implements model for email boxes"""

    __tablename__ = "email_boxes"

    id = Column(BigInteger, primary_key=True, unique=True, autoincrement=True)
    owner_id = Column(BigInteger, nullable=False)
    forum_id = Column(BigInteger, nullable=False)
    last_handled_email_id = Column(BigInteger, nullable=False, default=0)
    is_active = Column(Boolean, default=True)

    def __repr__(self) -> str:
        return f"Emailbox: {self.id} | Owner ID: {self.owner_id}, Forum ID: {self.forum_id}, " \
               f"Last handled email ID: {self.last_handled_email_id}, Is active: {self.is_active}"


class EmailAuthData(Base):
    """Implements model for email auth datas"""

    __tablename__ = "email_auths"

    emailbox_id = Column(BigInteger, primary_key=True, nullable=False)
    email_server_id = Column(LargeBinary, nullable=False)
    email_address = Column(LargeBinary, nullable=False)
    email_password = Column(LargeBinary, nullable=False)

    def __repr__(self) -> str:
        return f"EmailAuthData for {self.emailbox_id} | Email server ID: {self.email_server_id}, " \
               f"Email address: {self.email_address}, Email password: {self.email_password}"
