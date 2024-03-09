from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import exc
from app.exceptions.repo import DBError, ModelExists
from app.models.email import Emailbox as DBEmailbox
from app.entities.email import EncryptedEmailbox
from app.services.cryptography.cryptographer import EmailCryptographer


class EmailRepo:
    """Implements repository for emailbox entity"""

    def __init__(self, session: AsyncSession, crypto: EmailCryptographer) -> None:
        self._session = session
        self._crypto = crypto

    async def add_emailbox(self, emailbox: EncryptedEmailbox, update_if_exists: bool = False) -> None:
        db_emailbox = _convert_emailbox_to_db_emailbox(emailbox)
        try:
            if update_if_exists:
                await self._session.merge(db_emailbox)
            else:
                self._session.add(db_emailbox)
            await self._session.commit()
        except exc.IntegrityError as e:
            raise ModelExists("Adding model {model} failed".format(model=str(db_emailbox))) from e
        except exc.DatabaseError as e:
            raise DBError("Adding model {model} failed".format(model=str(db_emailbox))) from e

    # TODO: set_forum method overloading via singledispatch


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
        forum_id=int(str(db_emailbox.forum_id)),
        last_fetched_email_id=int(str(db_emailbox.last_fetched_email_id)),
        enabled=bool(db_emailbox.enabled),
    )
