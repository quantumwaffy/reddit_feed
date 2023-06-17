import asyncio
from typing import Generator
from uuid import uuid4

import pytest
from fastapi import FastAPI
from starlette.testclient import TestClient
from tortoise.contrib.fastapi import register_tortoise

from core.main import get_app
from core.settings import SETTINGS
from feed import models


@pytest.fixture(scope="module")
def test_app() -> Generator[TestClient, None, None]:
    app: FastAPI = get_app()

    register_tortoise(
        app,
        config=SETTINGS.ORM.test_config,
        generate_schemas=True,
        add_exception_handlers=True,
    )

    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture(scope="module")
def event_loop(test_app: TestClient) -> asyncio.AbstractEventLoop:
    asyncio.set_event_loop(asyncio.new_event_loop())
    loop: asyncio.AbstractEventLoop = asyncio.get_event_loop()
    return loop


@pytest.fixture(scope="module")
def subreddit(event_loop: asyncio.AbstractEventLoop) -> models.Subreddit:
    return event_loop.run_until_complete(models.Subreddit.create(name=f"subreddit_{uuid4().hex}"))
