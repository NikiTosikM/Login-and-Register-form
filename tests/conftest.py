from httpx import AsyncClient, ASGITransport

from pydantic_settings import BaseSettings, SettingsConfigDict

import pytest

from src.app import app
from src.database import  create_session

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy import text
from sqlalchemy.orm import DeclarativeBase

import asyncio

import os


class Settings(BaseSettings):
    USER_DATABASE: str
    USER_PASSWORD: str
    HOST: str
    PORT: str
    DATABASE_NAME: str
    SECRET_JWT: str
    JWT_ALGORITHM: str

    TEST_USER_DATABASE: str
    TEST_USER_PASSWORD: str
    TEST_HOST: str
    TEST_PORT: str
    TEST_DATABASE_NAME: str
    
    def connect_test_db(self):
        return f"postgresql+asyncpg://{self.TEST_USER_DATABASE}:\
    {self.TEST_USER_PASSWORD}@{self.TEST_HOST}:{self.TEST_PORT}/{self.TEST_DATABASE_NAME}"

    def connect_db(self):
        return  f"postgresql+asyncpg://{self.USER_DATABASE}:{self.USER_PASSWORD}@{self.HOST}:{self.PORT}/{self.DATABASE_NAME}"
    
    model_config = SettingsConfigDict(env_file="../.env")

path_true = os.path.join(os.path.dirname(__file__), '../.env')
print(os.path.exists(path_true)) 
# выдает True

setting = Settings()


class Base(DeclarativeBase):
    pass


async_engine_test = create_async_engine(setting.connect_db())
async_session_test = async_sessionmaker(async_engine_test)
Base.metadata.bind = async_engine_test


async def override_get_async_session():
    async with async_engine_test() as session:
        yield session

async_engine = create_async_engine(setting.connect_test_db())
async_session = async_sessionmaker(async_engine)

async def check_connection():
    async with async_session() as session:
        try:
            # Выполняем простой запрос для проверки соединения
            result = await session.execute(text("SELECT 1"))
            print("Соединение успешно установлено:", result.scalar())
        except Exception as e:
            print("Ошибка при подключении к базе данных:", e)

# Запускаем функцию
asyncio.run(check_connection())

app.dependency_overrides[create_session] = override_get_async_session


@pytest.fixture(scope="session")
async def ac():
    async with AsyncClient(transport=ASGITransport(app=app)) as ac:
        yield ac

