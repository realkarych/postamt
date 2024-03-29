from dataclasses import dataclass
from enum import Enum
from mailparser import MailParser
from pydantic import BaseModel, EmailStr, SecretStr
from typing import Optional
from app.entities import base
from app.services.cryptography.cryptographer import EmailCryptographer
from aiogram.filters.callback_data import CallbackData


class EmailUser(BaseModel):
    """Represents email user (sender or recipient)"""

    email: EmailStr
    name: Optional[str] = None

    class Config:
        frozen = True


class IncomingEmail(BaseModel):
    """Represents income email via IMAP protocol"""

    id_: str
    sender: EmailUser
    recipient: EmailUser
    content: MailParser  # Provided by mailparser lib

    class Config:
        frozen = True
        arbitrary_types_allowed = True


class EmailAuthData(BaseModel):
    """
    Represents email user (sender or recipient) authentication data
    Remember: password is a generated smtp/imap-key in email server app, not a password from email account
    """

    email: EmailStr
    password: SecretStr

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
        title="Office 365",
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


def get_server_by_id(id_: str) -> EmailServers:
    """Returns email server by id"""
    for server in EmailServers:
        if server.value.id_ == id_:
            return server
    raise ValueError(f"Email server with id '{id_}' not found")


@dataclass(frozen=True, slots=True)
class DecryptedEmailbox(base.DecryptedModel):

    crypto: EmailCryptographer

    owner_id: int
    server_id: str
    address: EmailStr
    password: SecretStr
    forum_id: int | None = None
    last_fetched_email_id: int | None = None
    enabled: bool | None = None
    db_id: int | None = None

    def encrypt(self) -> "EncryptedEmailbox":
        return EncryptedEmailbox(
            crypto=self.crypto,
            owner_id=self.owner_id,
            server_id=self.crypto.encrypt_key(self.server_id),
            address=self.crypto.encrypt_key(self.address),
            password=self.crypto.encrypt_key(self.password.get_secret_value()),
            forum_id=self.forum_id,
            last_fetched_email_id=self.last_fetched_email_id,
            enabled=self.enabled,
            db_id=self.db_id,
        )


@dataclass(frozen=True, slots=True)
class EncryptedEmailbox(base.EncryptedModel):

    crypto: EmailCryptographer

    owner_id: int
    server_id: bytes
    address: bytes
    password: bytes
    forum_id: int | None = None
    last_fetched_email_id: int | None = None
    enabled: bool | None = None
    db_id: int | None = None

    def decrypt(self) -> "DecryptedEmailbox":
        return DecryptedEmailbox(
            crypto=self.crypto,
            owner_id=self.owner_id,
            server_id=self.crypto.decrypt_key(self.server_id),
            address=self.crypto.decrypt_key(self.address),
            password=SecretStr(self.crypto.decrypt_key(self.password)),
            forum_id=self.forum_id,
            last_fetched_email_id=self.last_fetched_email_id,
            enabled=self.enabled,
            db_id=self.db_id,
        )


class EmailServerCallbackFactory(CallbackData, prefix="email_server"):

    server_id: str
