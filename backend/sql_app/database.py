import os

from typing import cast

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from starlette.requests import Request

DB_HOSTNAME = os.getenv("DB_HOSTNAME")

# SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./sql_app.db"
SQLALCHEMY_DATABASE_URL = f"postgresql+asyncpg://admin:123@{DB_HOSTNAME}/rinha"

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL, pool_size=20
)


class Base(DeclarativeBase):
    pass


def get_session(request: Request) -> AsyncSession:
    return cast(AsyncSession, request.state.db_session)
