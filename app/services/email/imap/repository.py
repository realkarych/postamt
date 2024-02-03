from app.services.email.imap.session import ImapSession


class ImapRepository:
    """A repository for working with IMAP protocol."""

    def __init__(self, session: ImapSession) -> None:
        self._session = session
