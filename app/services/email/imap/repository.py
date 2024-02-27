import logging
from pathlib import Path
from typing import Any, AsyncGenerator, Generator, Iterable
from app.entities.email import EmailUser, IncomingEmail
from app.exceptions.email import BadResponse
from app.services.email.imap.session import ImapSession
from mailparser import mailparser
from contextlib import contextmanager
import tempfile

from app.utils import paths
from os import listdir, path


class ImapRepository:
    """A repository for working with IMAP protocol."""

    def __init__(self, session: ImapSession, user: EmailUser) -> None:
        self._session = session
        self._user = user

    async def fetch_emails(self, email_ids: Iterable[str]) -> AsyncGenerator[IncomingEmail, Any]:
        """Fetch emails from the server"""
        for email_id in email_ids:
            logging.info(f"Fetching email with id={email_id}")
            try:
                email_bytes = await self._session.fetch_email(email_id)
            except BadResponse as e:
                logging.warn("{}\nFor email ids: {}".format(e, email_ids))
                continue
            email_content = mailparser.parse_from_bytes(email_bytes)
            yield IncomingEmail(
                id_=email_id,
                content=email_content,
                recipient=self._user,
                sender=EmailUser(email=str(email_content.from_[0][1]), name=str(email_content.from_[0][0])),
            )

    async def get_first_email_ids(self, count: int = 1) -> list[str]:
        """Get the first sent email ids from the server"""
        all_ids = await self._get_all_email_ids()
        return [str(id_) for id_ in all_ids[:count]]

    async def get_last_email_ids(self, count: int = 1) -> list[str]:
        """Get the last sent email ids from the server"""
        all_ids = await self._get_all_email_ids()
        logging.info("All found email ids: {}".format(all_ids))
        return [str(id_) for id_ in all_ids[-count:]]

    async def select_folder(self, folder: str) -> None:
        """Selects a folder in the mailbox. Default is INBOX"""
        await self._session.select_folder(folder)

    async def _get_all_email_ids(self) -> list[str]:
        """Get email ids from the server in ascending order"""
        return await self._session.select_email_ids()

    @contextmanager
    def load_attachments(self, email: IncomingEmail) -> Generator[list[Path], Any, Any]:
        """
        Creates temporary directory and loads email attachments.
        Returns list of file abspaths.
        Removes directory after exit contextmanager.
        """
        dest = str(paths.TEMPORARY_ATTACHMENTS_DIR)
        attachments_dir = tempfile.TemporaryDirectory(dir=dest)
        email.content.write_attachments(attachments_dir)
        try:
            yield [Path(f) for f in listdir(dest) if path.isfile(path.join(dest, f))]
        finally:
            attachments_dir.cleanup()
