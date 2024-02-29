from dataclasses import dataclass
from pydantic import EmailStr
from app.entities import base
from app.services.cryptography.cryptographer import TopicCryptographer


@dataclass(frozen=True, slots=True)
class DecryptedTopic(base.DecryptedModel):

    _crypto: TopicCryptographer

    forum_id: int
    topic_id: int
    topic_title: EmailStr

    def encrypt(self) -> "EncryptedTopic":
        return EncryptedTopic(
            _crypto=self._crypto,
            forum_id=self.forum_id,
            topic_id=self.topic_id,
            topic_title=self._crypto.encrypt_key(content=self.topic_title),
        )


@dataclass(frozen=True, slots=True)
class EncryptedTopic(base.EncryptedModel):

    _crypto: TopicCryptographer

    forum_id: int
    topic_id: int
    topic_title: bytes

    def decrypt(self) -> "DecryptedTopic":
        return DecryptedTopic(
            _crypto=self._crypto,
            forum_id=self.forum_id,
            topic_id=self.topic_id,
            topic_title=self._crypto.decrypt_key(code=self.topic_title),
        )
