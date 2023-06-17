from typing import Generator
from uuid import uuid4

import pytest
from httpx import AsyncClient
from tortoise import Tortoise

from core.main import app
from core.settings import SETTINGS
from feed import models as feed_models


@pytest.fixture(scope="session")
def anyio_backend() -> str:
    return "asyncio"


@pytest.fixture(scope="session")
async def client() -> Generator[AsyncClient, None, None]:
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


@pytest.fixture(scope="session", autouse=True)
async def initialize_tests() -> Generator[None, None, None]:
    await Tortoise.init(config=SETTINGS.ORM.test_config, _create_db=True)
    await Tortoise.generate_schemas()
    yield
    await Tortoise._drop_databases()


@pytest.fixture(scope="session")
async def subreddit() -> feed_models.Subreddit:
    return await feed_models.Subreddit.create(name=f"subreddit_{uuid4().hex}")
