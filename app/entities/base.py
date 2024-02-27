from abc import ABCMeta, abstractmethod


class ModelWithDBMixin(metaclass=ABCMeta):
    """Base model with database mixin"""

    pass


class DecryptedModel(ModelWithDBMixin):
    """Model with database mixin for decrypted data"""

    @abstractmethod
    def encrypt(self) -> "EncryptedModel":
        pass


class EncryptedModel(ModelWithDBMixin):
    """Model with database mixin for encrypted data"""

    @abstractmethod
    def decrypt(self) -> "DecryptedModel":
        pass
