import contextlib

from collections.abc import AsyncGenerator
from collections.abc import Generator
from datetime import datetime
from typing import ContextManager

from sqlalchemy import text
from sqlalchemy.engine import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import Session


from app.utils.config import configs


SYNC_DB_API = "psycopg2"
ASYNC_DB_API = "asyncpg"

# global so we don't create more than one engine per process
# outside of being best practice, this is needed so we can properly pool
# connections and not create a new pool on every request
_SYNC_ENGINE: Engine | None = None
_ASYNC_ENGINE: AsyncEngine | None = None


def get_db_current_time(db_session: Session) -> datetime:
    """Get the current time from Postgres representing the start of the transaction
    Within the same transaction this value will not update
    This datetime object returned should be timezone aware, default Postgres timezone is UTC
    """
    result = db_session.execute(text("SELECT NOW()")).scalar()
    if result is None:
        raise ValueError("Database did not return a time")
    return result


def build_connection_string(
    *,
    db_api: str = ASYNC_DB_API,
    user: str = configs.DATABASE_USERNAME,
    password: str = configs.POSTGRES_PASSWORD,
    host: str = configs.DATABASE_HOSTNAME,
    port: str = configs.DATABASE_PORT,
    db: str = configs.POSTGRES_DB,
) -> str:
    return f"postgresql+{db_api}://{user}:{password}@{host}:{port}/{db}"


def get_sqlalchemy_engine() -> Engine:
    global _SYNC_ENGINE
    if _SYNC_ENGINE is None:
        connection_string = build_connection_string(db_api=SYNC_DB_API)
        _SYNC_ENGINE = create_engine(connection_string, pool_size=40, max_overflow=10)
    return _SYNC_ENGINE


def get_sqlalchemy_async_engine() -> AsyncEngine:
    global _ASYNC_ENGINE
    if _ASYNC_ENGINE is None:
        connection_string = build_connection_string()
        _ASYNC_ENGINE = create_async_engine(
            connection_string, pool_size=40, max_overflow=10
        )
    return _ASYNC_ENGINE


def get_session_context_manager() -> ContextManager[Session]:
    return contextlib.contextmanager(get_session)()


def get_session() -> Generator[Session, None, None]:
    with Session(get_sqlalchemy_engine(), expire_on_commit=False) as session:
        yield session


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSession(
        get_sqlalchemy_async_engine(), expire_on_commit=False
    ) as async_session:
        yield async_session
