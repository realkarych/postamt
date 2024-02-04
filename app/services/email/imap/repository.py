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
