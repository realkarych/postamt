import asyncio
from contextlib import suppress
from app.entities.email import EmailAuthData, EmailServer, EmailServers
import aioimaplib

from app.exceptions.email import BadResponse, ImapConnectionFailed


_CONNECTION_ATTEMPTS = 10  # Number of times to attempt to connect to the IMAP server. If not -> connection error
_CONNECTION_ATTEMPTS_DELAY = 0.1  # Delay between connection attempts (in seconds)


class ImapSession:
    """A wrapper around aioimaplib connector that connects to Inboxes"""

    def __init__(self, server: EmailServers, auth_data: EmailAuthData) -> None:
        self._server: EmailServer = server.value
        self._auth_data = auth_data

    async def __aenter__(self) -> "ImapSession":
        for _ in range(_CONNECTION_ATTEMPTS):
            with suppress(TimeoutError):
                self._session = aioimaplib.IMAP4_SSL(
                    host=self._server.imap.host,
                    port=self._server.imap.port,
                )
                await self._try_login()
                if self._session.get_state() in ("AUTH", "SELECTED", "AUTHENTICATED"):
                    await self.select_folder()
                    break
            # If connection failed, wait and try again
            await asyncio.sleep(_CONNECTION_ATTEMPTS_DELAY)
        # If connection failed _CONNECTION_ATTEMPTS times, raise an exception
        else:
            raise ImapConnectionFailed("Failed to connect to the server ({server}) with auth_data={self._auth_data}")

        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self._session.logout()

    async def select_folder(self, folder: str = "INBOX") -> None:
        """Selects a folder in the mailbox"""
        await self._session.select(mailbox=folder)

    async def select_email_ids(self, flag: str = "ALL") -> list[str]:
        """
        Returns a tuple of email ids that match the given flag in ascending ids order:
        the newest email id is the last in the list
        """
        status, data = await self._session.search(flag)
        email_ids = [str(i[0]) for i in data[0].split()]
        if not email_ids:
            return []
        # API has a bug: last email id is not present in the list
        # so we add it manually
        if email_ids:
            email_ids.append(str(int(email_ids[-1]) + 1))
        return email_ids if status == "OK" else []

    async def fetch_email(self, email_id: str) -> bytes:
        """Fetches email by it's id in mailbox and returns it's content as bytes"""
        return await self._fetch_email(email_id)

    async def _fetch_email(self, email_id: str) -> bytes:
        status, data = await self._session.fetch(email_id, "(RFC822)")
        if status == "OK":
            try:
                return data[1]
            except IndexError:
                pass
        raise BadResponse(
            f"Bad response from server ({self._server}): auth_data={self._auth_data}, status={status}, data={data}, "
            f"email_id={email_id}"
        )

    async def _try_login(self) -> None:
        """Attempts to login to the server"""
        await self._session.wait_hello_from_server()
        await self._session.login(
            user=str(self._auth_data.email),
            password=self._auth_data.password.get_secret_value(),
        )
