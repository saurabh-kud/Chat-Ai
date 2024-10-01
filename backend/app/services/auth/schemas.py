import uuid
from enum import Enum

from fastapi_users import schemas


class UserRole(str, Enum):
    BASIC = "basic"
    ADMIN = "admin"


class UserRead(schemas.BaseUser[uuid.UUID]):
    full_name: str
    role: UserRole


class UserCreate(schemas.BaseUserCreate):
    full_name: str
    role: UserRole = UserRole.BASIC


class UserUpdate(schemas.BaseUserUpdate):
    full_name: str
    role: UserRole
