import os
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

# Supabase gives you a *full* Postgres URL, often starting with “postgres://”
# SQLAlchemy needs the asyncpg dialect → replace the scheme.
raw_url = os.environ["SUPABASE_DB_URL"]
DATABASE_URL = raw_url.replace("postgres://", "postgresql+asyncpg://", 1)

engine = create_async_engine(DATABASE_URL, pool_size=10, max_overflow=2)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)
