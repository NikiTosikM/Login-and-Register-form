from httpx import AsyncClient, ASGITransport

from pydantic_settings import BaseSettings, SettingsConfigDict

import pytest

from src.app import app
from src.database import  create_session

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy import text
from sqlalchemy.orm import DeclarativeBase

import os


class Settings(BaseSettings):
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

setting = Settings()


class Base(DeclarativeBase):
    pass


async_engine_test = create_async_engine(setting.connect_db())
async_session_test = async_sessionmaker(async_engine_test)
Base.metadata.bind = async_engine_test


async def override_get_async_session():
    async with async_engine_test() as session:
        yield session

app.dependency_overrides[create_session] = override_get_async_session


@pytest.fixture(scope="session")
async def ac():
    async with AsyncClient(transport=ASGITransport(app=app)) as ac:
        yield ac

