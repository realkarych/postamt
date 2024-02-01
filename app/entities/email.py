from enum import Enum
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


class EmailServerData(BaseModel):
    """Represents email server (smtp or imap) connection settings"""

    host: str
    port: int

    class Config:
        frozen = True


class EmailServer(BaseModel):
    """Represents email server (smtp or imap)"""

    id_: str  # Unique id of email server
    title: str  # Represents email server title
    imap: EmailServerData  # Represents imap connection settings
    smtp: EmailServerData  # Represents smtp connection settings

    def __str__(self) -> str:
        return self.title

    class Config:
        frozen = True


class EmailServers(Enum):
    """Represents supported email servers"""

    GMAIL = EmailServer(
        id_="gmail",
        title="Gmail",
        imap=EmailServerData(host="imap.gmail.com", port=993),
        smtp=EmailServerData(host="smtp.gmail.com", port=465),
    )
    YANDEX = EmailServer(
        id_="yandex",
        title="Yandex",
        imap=EmailServerData(host="imap.yandex.ru", port=993),
        smtp=EmailServerData(host="smtp.yandex.ru", port=465),
    )
    MAILRU = EmailServer(
        id_="mailru",
        title="Mail.ru",
        imap=EmailServerData(host="imap.mail.ru", port=993),
        smtp=EmailServerData(host="smtp.mail.ru", port=465),
    )
    ICLOUD = EmailServer(
        id_="icloud",
        title="iCloud",
        imap=EmailServerData(host="imap.mail.me.com", port=993),
        smtp=EmailServerData(host="smtp.mail.me.com", port=587),
    )
    OUTLOOK = EmailServer(
        id_="outlook",
        title="Outlook",
        imap=EmailServerData(host="imap-mail.outlook.com", port=993),
        smtp=EmailServerData(host="smtp-mail.outlook.com", port=587),
    )
    OFFICE365 = EmailServer(
        id_="office365",
        title="Office365",
        imap=EmailServerData(host="outlook.office365.com", port=993),
        smtp=EmailServerData(host="smtp.office365.com", port=587),
    )
    YAHOO = EmailServer(
        id_="yahoo",
        title="Yahoo",
        imap=EmailServerData(host="imap.mail.yahoo.com", port=993),
        smtp=EmailServerData(host="smtp.mail.yahoo.com", port=465),
    )

    def __str__(self) -> str:
        return str(self.value)


def get_server_by_id(id_: str) -> EmailServer:
    """Returns email server by id"""
    for server in EmailServers:
        if server.value.id_ == id_:
            return server.value
    raise ValueError(f"Email server with id '{id_}' not found")
