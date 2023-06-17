import pytest
from fastapi import status
from httpx import AsyncClient, Response

from core.settings import SETTINGS
from feed import test_data_generator


@pytest.mark.anyio
async def test_get_feed(client: AsyncClient):
    page_posts_count: int = SETTINGS.FEED.PAGE_SIZE + 1
    await test_data_generator.create_test_data(page_posts_count, 40, 10)
    response: Response = await client.get("/api/v1/feed/")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) < page_posts_count


@pytest.mark.anyio
async def test_create_test_feed(client: AsyncClient):
    data: dict[str, int] = {
        "post_count": SETTINGS.FEED.PAGE_SIZE,
        "promoted_percent": 50,
        "nsfw_percent": 20,
    }
    response: Response = await client.post("/api/v1/test/create", json=data)
    assert response.status_code == status.HTTP_201_CREATED
