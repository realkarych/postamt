from app.entities.email import EmailAuthData, EmailServers


_CONNECTION_ATTEMPTS = 5  # Number of times to attempt to connect to the IMAP server. If not -> connection error


class ImapSession:
    """A wrapper around aioimaplib connector that connects to Inboxes"""

    def __init__(self, imap_server: EmailServers, auth_data: EmailAuthData) -> None:
        self._imap_server = imap_server
        self._auth_data = auth_data

    def __aenter__(self) -> "ImapSession":
        return self

    def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        # TODO: close connection
        pass
