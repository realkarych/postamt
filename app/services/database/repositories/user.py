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

    def __init__(self, session: AsyncSession):
        self._session = session

    async def add_user(self, user: User, force_merge: bool = False):
        """
        Adds user to the database
        :param force_merge: If True, will merge (force update, rewrite) user into the database
        """
        async with self._session.begin():
            try:
                db_user = _convert_user_to_db_user(user)
                if force_merge:
                    logging.info("Merging user: %s", db_user)
                    await self._session.merge(db_user)
                else:
                    self._session.add(db_user)
                await self._session.flush()

            except IntegrityError as e:
                await self._session.rollback()
                logging.info("Failed to add user to the database. User already exists: %s", e)
                raise ModelExists("Failed to add user to the database") from e
            except SQLAlchemyError as e:
                await self._session.rollback()
                logging.error("Failed to add user to the database: %s", e)
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
    # I'm not stupid, `is not None` is needed here because sqlalchemy returns NoReturn.
    # Pyright, please, don't be so strict.
    return User(
        id_=int(str(db_user.id)),
        username=str(db_user.username) if db_user.username is not None else None,
        firstname=str(db_user.firstname) if db_user.firstname is not None else None,
        lastname=str(db_user.lastname) if db_user.lastname is not None else None,
        registered_date=db_user.registered_date if db_user.registered_date is not None else None,  # pyright: ignore
    )
