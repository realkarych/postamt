from dataclasses import dataclass
from aiogram import types
from typing import Optional

from app.entities import base


@dataclass(frozen=True, slots=True)
class User(base.ModelWithDBMixin):
    """Represents user entity"""

    id_: int  # Telegram user id
    username: Optional[str] = None  # Telegram username
    first_name: Optional[str] = None  # Telegram first name
    last_name: Optional[str] = None  # Telegram last name

    @classmethod
    def from_message(cls, message: types.Message) -> "User":
        """Creates User entity from message"""
        if not message.from_user:
            raise ValueError("Message does not have user")
        return cls(
            id_=message.from_user.id,
            username=message.from_user.username,
            first_name=message.from_user.first_name,
            last_name=message.from_user.last_name,
        )
