import logging
from typing import Any, AsyncGenerator, Iterable
from app.services.email.imap.session import ImapSession


class ImapRepository:
    """A repository for working with IMAP protocol."""

    def __init__(self, session: ImapSession) -> None:
        self._session = session

    async def fetch_emails(self, email_ids: Iterable[str]) -> AsyncGenerator[bytes, Any]:
        """Fetch emails from the server"""
        for email_id in email_ids:
            logging.info(f"Fetching email with id={email_id}")
            yield await self._session.fetch_email(email_id)

    async def get_all_email_ids(self) -> list[str]:
        """Get email ids from the server"""
        return await self._session.select_email_ids()

    async def get_first_email_ids(self, count: int = 1) -> list[str]:
        """Get the first sent email ids from the server"""
        all_ids = await self.get_all_email_ids()
        return [str(id_) for id_ in all_ids[:count]]

    async def get_last_email_ids(self, count: int = 1) -> list[str]:
        """Get the last sent email ids from the server"""
        all_ids = await self.get_all_email_ids()
        return [str(id_) for id_ in all_ids[-count:]]

    async def select_folder(self, folder: str) -> None:
        """Selects a folder in the mailbox. Default is INBOX"""
        await self._session.select_folder(folder)
