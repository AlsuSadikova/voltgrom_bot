import os
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from config import SQL_ALCHEMY
from database_voltgrom.models import Base

# DATABASE_URL = os.environ.get("SQL_ALCHEMY")
# print(DATABASE_URL)
# Создаём "движок" для БД
engine = create_async_engine(url=SQL_ALCHEMY, echo=True, pool_pre_ping=True)
# Подключение сессии для работы с БД
session_maker = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


# Создание таблиц с моделями
async def create_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# Удаление таблиц с моделями
async def drop_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
