from abc import ABCMeta, abstractmethod
from app.utils.config.consts import FERNET_KEYS_ENCODING
from cryptography.fernet import Fernet


def _encrypt_key(content: str, fernet_key: bytes) -> bytes:
    """Encrypts content with fernet key"""
    fernet = Fernet(fernet_key)
    token = fernet.encrypt(bytes(content, FERNET_KEYS_ENCODING))
    return token


def _decrypt_key(code: bytes, fernet_key: bytes) -> str:
    """Decrypts token with fernet key"""
    fernet = Fernet(fernet_key)
    token = fernet.decrypt(code)
    return token.decode(FERNET_KEYS_ENCODING)


class ICryptographer(metaclass=ABCMeta):
    """Abstract class for cryptography"""

    @abstractmethod
    def encrypt_key(self, content: str) -> bytes:
        """Encrypts content with fernet key"""
        raise NotImplementedError

    @abstractmethod
    def decrypt_key(self, code: bytes) -> str:
        """Decrypts token with fernet key"""
        raise NotImplementedError


class Cryptographer(ICryptographer):
    """Cryptography implementation"""

    def __init__(self, fernet_key: bytes) -> None:
        """Initializes fernet key from config"""
        self._fernet_key = fernet_key

    def encrypt_key(self, content: str) -> bytes:
        """Encrypts content with fernet key"""
        return _encrypt_key(content, self._fernet_key)

    def decrypt_key(self, code: bytes) -> str:
        """Decrypts token with fernet key"""
        return _decrypt_key(code, self._fernet_key)


class EmailCryptographer(Cryptographer):
    """Email cryptography implementation"""

    def __init__(self, fernet_key: bytes) -> None:
        """Initializes fernet key from config"""
        super().__init__(fernet_key)


class TopicCryptographer(Cryptographer):
    """Topic cryptography implementation"""

    def __init__(self, fernet_key: bytes) -> None:
        """Initializes fernet key from config"""
        super().__init__(fernet_key)
