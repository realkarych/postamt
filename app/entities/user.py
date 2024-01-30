from aiogram import types
from pydantic import BaseModel
from app.models.user import User as DBUser
from typing import Optional


class User(BaseModel):
    """User entity. Represents Telegram user and database user. Data Transfer Object"""

    id: int  # Telegram user id
    username: Optional[str] = None  # Telegram username
    first_name: Optional[str] = None  # Telegram first name
    last_name: Optional[str] = None  # Telegram last name

    def to_db_model(self) -> DBUser:
        """Converts User entity to database model"""
        return DBUser(
            id=self.id,
            username=self.username,
            firstname=self.first_name,
            lastname=self.last_name
        )

    @classmethod
    def from_message(cls, message: types.Message) -> 'User':
        """Creates User entity from message"""
        if not message.from_user:
            raise ValueError("Message does not have user")
        return cls(
            id=message.from_user.id,
            username=message.from_user.username,
            first_name=message.from_user.first_name,
            last_name=message.from_user.last_name
        )
