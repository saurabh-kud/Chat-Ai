from fastapi import APIRouter
from typing import Optional
from typing import List
from pydantic import BaseModel
from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from fastapi import Query
from sqlalchemy.orm import Session

from app.services.auth.schemas import UserRead
from app.services.auth.schemas import UserRole
from app.services.auth.users import current_admin_user
from app.services.auth.users import optional_valid_user
from app.db.engine import get_session
from app.db.models import User
from app.db.users import list_users
from app.db.users import search_users_by_email


router = APIRouter(prefix="/manage", tags=["users"])


@router.get("/users")
def list_all_users(
    _: User | None = Depends(current_admin_user),
    db_session: Session = Depends(get_session),
) -> list[UserRead]:
    users = list_users(db_session)
    return [UserRead.from_orm(user) for user in users]


class UserRoleResponse(BaseModel):
    role: str


class UserInfo(BaseModel):
    id: str
    full_name: str
    email: str
    is_active: bool
    is_superuser: bool
    is_verified: bool
    role: UserRole


@router.get("/me")
def verify_user_logged_in(user: User | None = Depends(optional_valid_user)) -> UserInfo:
    # NOTE: this does not use `current_user` / `current_admin_user` because we don't want
    # to enforce user verification here - the frontend always wants to get the info about
    # the current user regardless of if they are currently verified
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="User Not Authenticated"
        )

    return UserInfo(
        id=str(user.id),
        full_name=user.full_name,
        email=user.email,
        is_active=user.is_active,
        is_superuser=user.is_superuser,
        is_verified=user.is_verified,
        role=user.role,
    )


@router.get("/search-users-by-email")
def search_users_by_email_route(
    email: Optional[str] = Query(None, description="Email to search for"),
    _: User | None = Depends(current_admin_user),
    db_session: Session = Depends(get_session),
) -> List[UserRead]:
    users = search_users_by_email(db_session, email)
    return [UserRead(**user.__dict__) for user in users]
