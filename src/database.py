from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from config import setting


async_engine = create_async_engine(setting.connect_db())
async_session = async_sessionmaker(async_engine)


class Base(DeclarativeBase):
    pass


async def create_session():
    async with async_session() as session:
        yield session

