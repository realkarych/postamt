from click import Path
from pydantic import BaseModel, EmailStr
from typing import Optional
import datetime


class EmailUser(BaseModel):
    """Represents email user (sender or recipient)"""

    email: EmailStr
    name: Optional[str] = None

    class Config:
        frozen = True


class Email(BaseModel):
    """Represents email (income or outcome)"""

    id_: Optional[int] = None  # email id in user's Inbox
    sender: Optional[EmailUser] = None
    recipient: Optional[EmailUser] = None
    subject: Optional[str] = None  # email subject
    content: Optional[str] = None  # email content (normalized text in unicode utf-8)
    date: Optional[datetime.datetime] = None  # email date sent
    attachments_path: Optional[Path] = None  # Path to local temporary dir with email attachments

    class Config:
        frozen = True
