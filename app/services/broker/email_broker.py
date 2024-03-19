import asyncio
from app.entities.email import EmailAuthData, EmailUser, get_server_by_id
from app.services.cryptography.cryptographer import EmailCryptographer
from app.services.database.repositories.email import EmailRepo
from app.services.database.repositories.user import UserRepo
from sqlalchemy.ext.asyncio import async_sessionmaker
from app.services.email.imap.repository import ImapRepository
from app.services.email.imap.session import ImapSession
from app.services.broker import serializer, topics
from aiokafka import AIOKafkaProducer
from app.utils.config import consts


class EmailBroker:

    def __init__(
        self, producer: AIOKafkaProducer, sessionmaker: async_sessionmaker, email_crypto: EmailCryptographer
    ) -> None:
        self._sessionmaker = sessionmaker
        self._email_crypto = email_crypto
        self._producer = producer
        self._produce_emails_task = None

    async def start(self) -> None:
        """Starts email broker"""
        await self._start_produce_emails()

    async def stop(self) -> None:
        if self._produce_emails_task is not None:
            try:
                self._produce_emails_task.cancel()
            except asyncio.CancelledError:
                pass
            self._produce_emails_task = None

    async def _start_produce_emails(self) -> None:
        if self._produce_emails_task is None:
            self._produce_emails_task = asyncio.create_task(self._produce_emails())
        if self._produce_emails_task.done():
            self._produce_emails_task = None

    async def _produce_emails(self) -> None:
        async with self._sessionmaker() as session:
            self._email_repo = EmailRepo(session=session, crypto=self._email_crypto)
            self._user_repo = UserRepo(session=session)
            async for __encrypted_emailbox in self._email_repo.get_active_emailboxes():
                emailbox = __encrypted_emailbox.decrypt()
                async with ImapSession(
                    server=get_server_by_id(emailbox.server_id),
                    auth_data=EmailAuthData(email=emailbox.address, password=emailbox.password),
                ) as session:
                    user = await self._user_repo.get_user(user_id=emailbox.owner_id)
                    if not user:
                        raise ValueError(f"User with id={emailbox.owner_id} not found while fetching emailbox")
                    imap_repo = ImapRepository(
                        session=session, user=EmailUser(email=emailbox.address, name=user.firstname)
                    )
                    async for email in imap_repo.fetch_emails(
                        from_id=emailbox.last_fetched_email_id,  # type: ignore
                        limit=consts.EMAIL_CHUNK_LIMIT,
                    ):
                        dumped_email = email.model_dump()
                        await self._producer.send_and_wait(topics.SEND_EMAIL, serializer.to_bytes(data=dumped_email))
                        await self._email_repo.increment_last_email_id(emailbox_id=emailbox.db_id)  # type: ignore
