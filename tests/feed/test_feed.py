import asyncio

from fastapi import status
from httpx import Response
from starlette.testclient import TestClient

from core.settings import SETTINGS
from feed import test_data_generator


def test_get_feed(test_app: TestClient, event_loop: asyncio.AbstractEventLoop):
    page_posts_count: int = SETTINGS.FEED.PAGE_SIZE + 1
    event_loop.run_until_complete(test_data_generator.create_test_data(page_posts_count, 40, 10))
    response: Response = test_app.get("/api/v1/feed/")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) < page_posts_count


def test_create_test_feed(test_app: TestClient):
    data: dict[str, int] = {
        "post_count": SETTINGS.FEED.PAGE_SIZE,
        "promoted_percent": 50,
        "nsfw_percent": 20,
    }
    response: Response = test_app.post("/api/v1/test/create", json=data)
    assert response.status_code == status.HTTP_201_CREATED
