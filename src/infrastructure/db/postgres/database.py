from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from src.infrastructure.db.postgres.settings import postgres_settings

engine = create_async_engine(postgres_settings.DB_URL_ASYNC)
new_async_session = async_sessionmaker(bind=engine, expire_on_commit=False)

engine_null_pool = create_async_engine(postgres_settings.DB_URL_ASYNC, poolclass=NullPool)
new_async_session_null_pool = async_sessionmaker(bind=engine_null_pool, expire_on_commit=False)
