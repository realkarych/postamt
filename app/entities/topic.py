from dataclasses import dataclass
from pydantic import EmailStr
from app.entities import base
from app.services.cryptography.cryptographer import EmailCryptographer


@dataclass(frozen=True, slots=True)
class DecryptedTopic(base.DecryptedModel):

    forum_id: int
    topic_id: int
    topic_title: EmailStr

    def encrypt(self) -> "EncryptedTopic":
        crypto = EmailCryptographer()
        return EncryptedTopic(
            forum_id=self.forum_id, topic_id=self.topic_id, topic_title=crypto.encrypt_key(content=self.topic_title)
        )


@dataclass(frozen=True, slots=True)
class EncryptedTopic(base.EncryptedModel):

    forum_id: int
    topic_id: int
    topic_title: bytes

    def decrypt(self) -> "DecryptedTopic":
        crypto = EmailCryptographer()
        return DecryptedTopic(
            forum_id=self.forum_id, topic_id=self.topic_id, topic_title=crypto.decrypt_key(code=self.topic_title)
        )
