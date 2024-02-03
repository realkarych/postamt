from app.services.email.imap.session import ImapSession


class ImapRepo:

    def __init__(self, session: ImapSession) -> None:
        self._session = session

    async def select_email_ids(self):
        await self._session.select_email_ids()
