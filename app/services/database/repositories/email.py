from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from app.exceptions.repo import DBError, ModelExists
from app.models.email import EmailBox as DBEmailBox, EmailAuthData as DBEmailAuthData
from app.entities.email import EmailBox, DecryptedEmailAuthData, EncryptedEmailAuthData
from app.services.cryptography.cryptographer import EmailCryptographer


class EmailRepo:
    """Implements repository for email entity"""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def add_emailbox(self, emailbox: EmailBox, auth_data: DecryptedEmailAuthData) -> None:
        """Adds email box to database"""
        async with self._session.begin():
            try:
                db_emailbox = _convert_emailbox_to_db_emailbox(emailbox)
                db_auth_data = _convert_auth_data_to_db_auth_data(auth_data.encrypt())
                self._session.add(db_emailbox)
                self._session.add(db_auth_data)
                await self._session.flush()

            except IntegrityError as e:
                await self._session.rollback()
                raise ModelExists("Failed to add emailbox to the database") from e
            except SQLAlchemyError as e:
                await self._session.rollback()
                raise DBError("Failed to add emailbox to the database") from e

    async def get_emailbox(
        self, crypto: EmailCryptographer, emailbox_id: int
    ) -> Optional[tuple[EmailBox, DecryptedEmailAuthData]]:
        """Gets email box from the database"""
        try:
            query = (
                select(DBEmailBox, DBEmailAuthData)
                .join(DBEmailAuthData, DBEmailAuthData.emailbox_id == DBEmailBox.id)
                .where(DBEmailBox.id == emailbox_id)
            )

            result = await self._session.execute(query)
            db_emailbox, db_auth_data = result.scalar_one()

            if not db_emailbox:
                return None
            # This case is wrong, raise an exception
            if not db_auth_data:
                raise DBError("Failed to get emailbox auth data from the database")

            emailbox = _convert_db_emailbox_to_emailbox(db_emailbox)
            auth_data = _convert_db_auth_data_to_auth_data(crypto, db_auth_data)
            return emailbox, auth_data.decrypt()
        except SQLAlchemyError as e:
            raise DBError("Failed to get emailbox from the database") from e


def _convert_emailbox_to_db_emailbox(emailbox: EmailBox) -> DBEmailBox:
    return DBEmailBox(
        id=emailbox.db_id,
        owner_id=emailbox.owner_id,
        forum_id=emailbox.forum_id,
        last_handled_email_id=emailbox.last_handled_email_id,
        is_active=emailbox.is_active,
    )


def _convert_db_emailbox_to_emailbox(db_emailbox: DBEmailBox) -> EmailBox:
    return EmailBox(
        db_id=int(str(db_emailbox.id)),
        owner_id=int(str(db_emailbox.owner_id)),
        forum_id=int(str(db_emailbox.forum_id)),
        last_handled_email_id=int(str(db_emailbox.last_handled_email_id)),
        is_active=bool(db_emailbox.is_active),
    )


def _convert_auth_data_to_db_auth_data(auth_data: EncryptedEmailAuthData) -> DBEmailAuthData:
    return DBEmailAuthData(
        emailbox_id=auth_data.emailbox_id,
        email_server_id=auth_data.email_server_id,
        email_address=auth_data.email_address,
        email_password=auth_data.email_password,
    )


def _convert_db_auth_data_to_auth_data(
    crypto: EmailCryptographer, db_auth_data: DBEmailAuthData
) -> EncryptedEmailAuthData:
    return EncryptedEmailAuthData(
        _crypto=crypto,
        emailbox_id=int(str(db_auth_data.emailbox_id)),
        email_server_id=bytes(db_auth_data.email_server_id),  # type: ignore
        email_address=bytes(db_auth_data.email_address),  # type: ignore
        email_password=bytes(db_auth_data.email_password),  # type: ignore
    )
