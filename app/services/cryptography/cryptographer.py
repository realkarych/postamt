from cryptography.fernet import Fernet
from abc import ABCMeta, abstractmethod
from app.utils.config import FERNET_KEYS_ENCODING, config


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


class Cryptographer(metaclass=ABCMeta):
    """Abstract class for cryptography"""

    @abstractmethod
    def encrypt_key(self, content: str) -> bytes:
        """Encrypts content with fernet key"""
        raise NotImplementedError

    @abstractmethod
    def decrypt_key(self, code: bytes) -> str:
        """Decrypts token with fernet key"""
        raise NotImplementedError


class EmailCryptographer(Cryptographer):
    """Cryptography for email"""

    def __init__(self) -> None:
        """Initializes fernet key from config"""
        self._fernet_key = config.EMAIL_FERNET_KEY

    def encrypt_key(self, content: str) -> bytes:
        """Encrypts content with fernet key"""
        return _encrypt_key(content, self._fernet_key)

    def decrypt_key(self, code: bytes) -> str:
        """Decrypts token with fernet key"""
        return _decrypt_key(code, self._fernet_key)
