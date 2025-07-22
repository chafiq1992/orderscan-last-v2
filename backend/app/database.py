from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
import os

DATABASE_URL = (
    f"postgresql+asyncpg://{os.environ['DB_USER']}:{os.environ['DB_PASS']}"
    f"@/{os.environ['DB_NAME']}?host=/cloudsql/{os.environ['INSTANCE_CONNECTION_NAME']}"
)

engine = create_async_engine(
    DATABASE_URL,
    pool_size=10,
    max_overflow=2,
)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)
