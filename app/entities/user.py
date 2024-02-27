from dataclasses import dataclass
from aiogram import types
from typing import Optional
from datetime import datetime

from app.entities import base


@dataclass(frozen=True, slots=True)
class User(base.ModelWithDBMixin):
    """Represents user entity"""

    id_: int  # Telegram user id
    username: Optional[str] = None  # Telegram username
    firstname: Optional[str] = None  # Telegram first name
    lastname: Optional[str] = None  # Telegram last name
    registered_date: Optional[datetime] = None  # Date of registration

    @classmethod
    def from_message(cls, message: types.Message) -> "User":
        """Creates User entity from message"""
        if not message.from_user:
            raise ValueError("Message does not have user")
        return cls(
            id_=message.from_user.id,
            username=message.from_user.username,
            firstname=message.from_user.first_name,
            lastname=message.from_user.last_name,
        )
