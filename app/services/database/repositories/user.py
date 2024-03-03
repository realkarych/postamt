import logging
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy import select
from app.exceptions.repo import DBError, ModelExists

from app.models.user import User as DBUser
from app.entities.user import User


class UserRepo:
    """Implements repository for user entity"""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def add_user(self, user: User, update_when_exists: bool = False) -> None:
        """
        Adds user to the database
        :param update_when_exists: If True, will merge (force update, rewrite) user into the database
        """
        try:
            db_user = _convert_user_to_db_user(user)
            if update_when_exists:
                logging.info("Merging user: %s", db_user)
                await self._session.merge(db_user)
            else:
                self._session.add(db_user)
            await self._session.commit()

        except IntegrityError as e:
            raise ModelExists("Failed to add user to the database") from e
        except SQLAlchemyError as e:
            raise DBError("Failed to add user to the database") from e

    async def get_user(self, user_id: int) -> Optional[User]:
        """Gets user from the database"""
        try:
            result = await self._session.execute(select(DBUser).where(DBUser.id == user_id))
            db_user = result.scalar_one_or_none()
            return _convert_db_user_to_user(db_user) if db_user else None
        except SQLAlchemyError as e:
            logging.error("Failed to get user from the database: %s", e)
            raise DBError("Failed to get user from the database") from e


def _convert_user_to_db_user(user: User) -> DBUser:
    return DBUser(
        id=user.id_,
        username=user.username,
        firstname=user.firstname,
        lastname=user.lastname,
        registered_date=user.registered_date,
    )


def _convert_db_user_to_user(db_user: DBUser) -> User:
    return User(
        id_=int(str(db_user.id)),
        username=str(db_user.username) if db_user.username else None,  # pyright: ignore
        firstname=str(db_user.firstname) if db_user.firstname else None,  # pyright: ignore
        lastname=str(db_user.lastname) if db_user.lastname else None,  # pyright: ignore
        registered_date=db_user.registered_date if db_user.registered_date else None,  # pyright: ignore
    )
