import json
import pytest_asyncio
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis

from httpx import AsyncClient
from sqlalchemy import insert, text

from app.core import Base, db_factory, settings, Blockchain, Block
from app.main import app


def open_mock_json(path: str):
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


async def insert_mock_data(model, values):
    async with db_factory.session_factory() as session:
        query = insert(model).values(values)
        await session.execute(query)
        await session.commit()


async def load_mock_blockchain():
    blockchains = open_mock_json("tests/mock/mock_blockchains.json")
    await insert_mock_data(Blockchain, blockchains)


async def load_mock_blocks():
    blocks = open_mock_json("tests/mock/mock_blocks.json")
    await insert_mock_data(Block, blocks)


@pytest_asyncio.fixture(scope="session", autouse=True)
async def prepare_database():
    assert settings.MODE == "TEST"

    async with db_factory.engine.begin() as session:
        await session.run_sync(Base.metadata.drop_all)
        await session.run_sync(Base.metadata.create_all)

    await load_mock_blockchain()
    await load_mock_blocks()


@pytest_asyncio.fixture(scope="function")
async def ac():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest_asyncio.fixture(scope="function")
async def session():
    async with db_factory.session_factory() as session:
        yield session


@pytest_asyncio.fixture
async def reset_blockchain():
    async with db_factory.session_factory() as session:
        await session.execute(text("DELETE FROM blocks"))
        await session.execute(text("DELETE FROM blockchain"))
        await session.commit()
    await load_mock_blockchain()
    await load_mock_blocks()


@pytest_asyncio.fixture(scope="session", autouse=True)
async def init_redis():
    redis = aioredis.from_url("redis://localhost")
    FastAPICache.init(RedisBackend(redis), prefix="blockchain")
