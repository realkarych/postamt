from app.entities.email import EmailAuthData, EmailUser, get_server_by_id
from app.services.database.repositories.email import EmailRepo
from app.services.database.repositories.user import UserRepo
from app.services.email.imap.repository import ImapRepository
from app.services.email.imap.session import ImapSession
from app.services.broker import serializer
from aiokafka import AIOKafkaProducer
from app.utils.config import consts
from app.utils.config.loader import kafka


class EmailboxBroker:

    def __init__(self, email_repo: EmailRepo, user_repo: UserRepo) -> None:
        self._email_repo = email_repo
        self._user_repo = user_repo
        self._producer = AIOKafkaProducer(bootstrap_servers=f"{kafka.host}:{kafka.port}")

    async def run(self, topic: str) -> None:
        await self._producer.start()
        try:
            async for encrypted_emailbox in self._email_repo.get_active_emailboxes():
                emailbox = encrypted_emailbox.decrypt()
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
                        from_id=encrypted_emailbox.last_fetched_email_id,  # type: ignore
                        limit=consts.EMAIL_CHUNK_LIMIT,
                    ):
                        dumped_email = email.model_dump()
                        await self._producer.send_and_wait(topic, serializer.to_bytes(data=dumped_email))

        finally:
            await self._producer.stop()
