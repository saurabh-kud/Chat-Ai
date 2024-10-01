from fastapi import HTTPException
from typing import Optional
from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from app.db.models import User

# from folderchat.db.models import User
# from folderchat.db.models import UserAllowedLLMModel
# from folderchat.utils.logger import setup_logger

# logger = setup_logger()


def list_users(db_session: Session) -> Sequence[User]:
    """List all users. No pagination as of now, as the # of users
    is assumed to be relatively small (<< 1 million)"""
    return db_session.scalars(select(User)).unique().all()


def search_users_by_email(
    db_session: Session, email: Optional[str] = None
) -> Sequence[User]:
    """Search users by email."""
    if email:
        return (
            db_session.scalars(select(User).where(User.email.ilike(f"%{email}%")))
            .unique()
            .all()
        )
    return []


def get_user_email(user_id: str, db_session: Session) -> str:
    """Get a user's email based on their ID"""
    stmt = select(User.email).where(User.id == user_id)
    try:
        result = db_session.execute(stmt).scalar_one()
    except NoResultFound:
        raise HTTPException(status_code=404, detail="User not found")

    return result


def get_user_by_email(email: str, db_session: Session) -> str:
    """Get a user based on their email"""
    stmt = select(User.id, User.role).where(User.email == email)
    try:
        return db_session.execute(stmt).unique().first()
    except NoResultFound:
        raise HTTPException(status_code=404, detail="User not found")
