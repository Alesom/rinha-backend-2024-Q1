import os

from sqlalchemy import AsyncAdaptedQueuePool
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

DB_HOSTNAME = os.getenv("DB_HOSTNAME")

# SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./sql_app.db"
SQLALCHEMY_DATABASE_URL = f"postgresql+asyncpg://admin:123@{DB_HOSTNAME}/rinha"

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_size=50,
    max_overflow=20,
    poolclass=AsyncAdaptedQueuePool,
)
session_maker = async_sessionmaker(bind=engine, expire_on_commit=False)


async def get_session() -> AsyncSession:
    async with session_maker.begin() as session:
        yield session
