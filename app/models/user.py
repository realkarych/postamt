from sqlalchemy import Column, BigInteger, String, DateTime, func

from app.services.database.base import Base


class User(Base):
    """Implements base table contains all registered in bot users"""

    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True, unique=True, autoincrement=False)  # Telegram id
    username = Column(String(32), default=None, unique=False)  # Telegram username without @
    firstname = Column(String(256), default=None, unique=False)  # Telegram first name
    lastname = Column(String(256), default=None, unique=False)  # Telegram last name
    registered_date = Column(DateTime(timezone=True), server_default=func.now())  # Date of /start command handling

    def __repr__(self) -> str:
        return f"User: {self.id} | @{self.username}, ({self.firstname}, {self.lastname}), {self.registered_date}"
