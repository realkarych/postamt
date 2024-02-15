import logging
from typing import Any, AsyncGenerator, Iterable
from app.entities.email import EmailUser, IncomingEmail
from app.services.email.imap.session import ImapSession
from mailparser import mailparser


class ImapRepository:
    """A repository for working with IMAP protocol."""

    def __init__(self, session: ImapSession, user: EmailUser) -> None:
        self._session = session
        self._user = user

    async def fetch_emails(self, email_ids: Iterable[str]) -> AsyncGenerator[IncomingEmail, Any]:
        """Fetch emails from the server"""
        for email_id in email_ids:
            logging.info(f"Fetching email with id={email_id}")
            email_bytes = await self._session.fetch_email(email_id)
            email_content = mailparser.parse_from_bytes(email_bytes)
            yield IncomingEmail(
                id_=email_id,
                content=email_content,
                recipient=self._user,
                sender=EmailUser(
                    email=str(email_content.from_[0][1]),
                    name=str(email_content.from_[0][0])
                )
            )

    async def get_first_email_ids(self, count: int = 1) -> list[str]:
        """Get the first sent email ids from the server"""
        all_ids = await self._get_all_email_ids()
        return [str(id_) for id_ in all_ids[:count]]

    async def get_last_email_ids(self, count: int = 1) -> list[str]:
        """Get the last sent email ids from the server"""
        all_ids = await self._get_all_email_ids()
        return [str(id_) for id_ in all_ids[-count:]]

    async def select_folder(self, folder: str) -> None:
        """Selects a folder in the mailbox. Default is INBOX"""
        await self._session.select_folder(folder)

    async def _get_all_email_ids(self) -> list[str]:
        """Get email ids from the server in ascending order"""
        return await self._session.select_email_ids()
