from sqlalchemy import Column, BigInteger, Boolean, LargeBinary
from app.services.database.base import Base


class EmailBox(Base):
    """Implements model for email boxes"""

    __tablename__ = "email_boxes"

    id = Column(BigInteger, primary_key=True, unique=True, autoincrement=True)
    server_id = Column(LargeBinary, nullable=False)  # Like `gmail`, `yandex` etc.
    address = Column(LargeBinary, nullable=False)  # email@domain. Encrypted.
    password = Column(LargeBinary, nullable=False)  # access key generated in account. Encrypted.
    owner_id = Column(BigInteger, nullable=False)  # Telegram id of emailbox owner.
    forum_id = Column(BigInteger, nullable=True, default=None)  # Emailbox works in Forum (supergroup).
    last_fetched_email_id = Column(BigInteger, nullable=False, default=0)  # Pointer of last fetched email.
    is_active = Column(Boolean, default=True)  # If auth data is non actual, I mark it as disabled and don't fetch.

    def __repr__(self) -> str:
        return (
            f"Emailbox: {self.id} | Owner ID: {self.owner_id} | Forum ID: {self.forum_id}\n"
            f"Server: {self.server_id} | Address: {self.address} | Password: {self.password}\n"
            f"Last fetched email ID: {self.last_fetched_email_id}, Is active: {self.is_active}"
        )
