import asyncio
from contextlib import suppress
import logging
from app.entities.email import EmailAuthData, EmailServer, EmailServers
import aioimaplib


_CONNECTION_ATTEMPTS = 10  # Number of times to attempt to connect to the IMAP server. If not -> connection error
_CONNECTION_ATTEMPTS_DELAY = 0.1  # Delay between connection attempts (in seconds)


class ImapSession:
    """A wrapper around aioimaplib connector that connects to Inboxes"""

    def __init__(self, server: EmailServers, auth_data: EmailAuthData) -> None:
        self._server: EmailServer = server.value
        self._auth_data = auth_data

    async def __aenter__(self) -> "ImapSession":
        while connection_attempt := 0 < _CONNECTION_ATTEMPTS:
            with suppress(TimeoutError):
                self._session = aioimaplib.IMAP4_SSL(
                    host=self._server.imap.host,
                    port=self._server.imap.port,
                )
                await self._session.wait_hello_from_server()
                await self._session.login(
                    user=str(self._auth_data.email),
                    password=self._auth_data.password,
                )
                # Connection successful
                if self._session.status == "AUTH":
                    break

            await asyncio.sleep(_CONNECTION_ATTEMPTS_DELAY)
            connection_attempt += 1

        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self._session.logout()

    async def select_folder(self, folder: str = "INBOX") -> None:
        await self._session.select(mailbox=folder)

    async def select_email_ids(self, flag: str = "ALL"):
        """Returns a tuple of email ids that match the given flag in ascending order"""
        status, data = await self._session.search(flag)
        logging.info(f"status: {status}, data: {data}")
