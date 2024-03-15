from sqlalchemy import update, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import exc
from app.exceptions.repo import DBError, ModelExists
from app.models.email import Emailbox as DBEmailbox
from app.entities.email import DecryptedEmailbox, EncryptedEmailbox
from app.services.cryptography.cryptographer import EmailCryptographer
from functools import singledispatchmethod


class EmailRepo:
    """Implements repository for emailbox entity"""

    def __init__(self, session: AsyncSession, crypto: EmailCryptographer) -> None:
        self._session = session
        self._crypto = crypto

    async def add_emailbox(self, emailbox: EncryptedEmailbox) -> None:
        if await self.emailbox_exists(emailbox.decrypt()):
            raise ModelExists("Emailbox {emailbox} already exists".format(emailbox=str(emailbox)))

        db_emailbox = _convert_emailbox_to_db_emailbox(emailbox)
        try:
            self._session.add(db_emailbox)
            await self._session.commit()
        except exc.IntegrityError as e:
            raise ModelExists("Adding model {model} failed".format(model=str(db_emailbox))) from e
        except exc.DatabaseError as e:
            raise DBError("Adding model {model} failed".format(model=str(db_emailbox))) from e

    @singledispatchmethod
    async def get_emailbox(self, emailbox_id: int) -> EncryptedEmailbox | None:
        query = select(DBEmailbox).where(DBEmailbox.id == emailbox_id)
        db_emailbox = (await self._session.execute(query)).scalar_one_or_none()
        if not db_emailbox:
            return None
        return _convert_db_emailbox_to_emailbox(self._crypto, db_emailbox)

    @get_emailbox.register
    async def _(self, emailbox: EncryptedEmailbox) -> EncryptedEmailbox | None:
        query = select(DBEmailbox).where(
            DBEmailbox.address == emailbox.address,
            DBEmailbox.password == emailbox.password,
            DBEmailbox.owner_id == emailbox.owner_id,
        )
        db_emailbox = (await self._session.execute(query)).scalar_one_or_none()
        if not db_emailbox:
            return None
        return _convert_db_emailbox_to_emailbox(self._crypto, db_emailbox)

    @get_emailbox.register
    async def _(self, user_id: int, forum_id: int) -> EncryptedEmailbox | None:
        query = select(DBEmailbox).where(
            DBEmailbox.owner_id == user_id,
            DBEmailbox.forum_id == forum_id,
        )
        db_emailbox = (await self._session.execute(query)).scalar_one_or_none()
        if not db_emailbox:
            return None
        return _convert_db_emailbox_to_emailbox(self._crypto, db_emailbox)

    async def get_emailbox_without_forum(self, user_id: int) -> EncryptedEmailbox | None:
        """Gets emailbox by user_id"""
        query = select(DBEmailbox).where(DBEmailbox.owner_id == user_id, DBEmailbox.forum_id == None)  # noqa
        result = await self._session.execute(query)
        db_emailbox = result.scalars().fetchall()
        if not db_emailbox:
            return None
        return _convert_db_emailbox_to_emailbox(self._crypto, db_emailbox[0])

    async def update_forum_id(self, emailbox_id: int, forum_id: int | None) -> None:
        """Updates forum_id for emailbox. forum_id=None resets value."""

        query = update(DBEmailbox).where(DBEmailbox.id == emailbox_id).values(forum_id=forum_id)
        await self._session.execute(query)
        await self._session.commit()

    async def emailbox_exists(self, emailbox: DecryptedEmailbox) -> bool:
        query = select(DBEmailbox).where(DBEmailbox.owner_id == emailbox.owner_id)
        user_emailboxes = [
            _convert_db_emailbox_to_emailbox(self._crypto, box).decrypt()
            for box in (await self._session.execute(query)).scalars()
        ]
        if not user_emailboxes:
            return False
        return any(box.password == emailbox.password and box.address == emailbox.address for box in user_emailboxes)


def _convert_emailbox_to_db_emailbox(emailbox: EncryptedEmailbox) -> DBEmailbox:
    return DBEmailbox(
        id=emailbox.db_id,
        server_id=emailbox.server_id,
        address=emailbox.address,
        password=emailbox.password,
        owner_id=emailbox.owner_id,
        forum_id=emailbox.forum_id,
        last_fetched_email_id=emailbox.last_fetched_email_id,
        enabled=emailbox.enabled,
    )


def _convert_db_emailbox_to_emailbox(crypto: EmailCryptographer, db_emailbox: DBEmailbox) -> EncryptedEmailbox:
    return EncryptedEmailbox(
        crypto=crypto,
        db_id=int(str(db_emailbox.id)),
        server_id=db_emailbox.server_id,
        address=bytes(db_emailbox.address),  # type: ignore
        password=bytes(db_emailbox.password),  # type: ignore
        owner_id=int(str(db_emailbox.owner_id)),
        forum_id=int(str(db_emailbox.forum_id)) if bool(db_emailbox.forum_id) else None,
        last_fetched_email_id=int(str(db_emailbox.last_fetched_email_id)),
        enabled=bool(db_emailbox.enabled),
    )
