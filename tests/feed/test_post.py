import pytest
from fastapi import status
from httpx import AsyncClient, Response

from core.settings import SETTINGS
from feed import models


@pytest.mark.anyio
async def test_create_post(client: AsyncClient, subreddit: models.Subreddit):
    data: dict[str, str | int | bool | None] = {
        "title": "test_title",
        "author": f"{SETTINGS.FEED.AUTHOR_PREFIX}test",
        "link": None,
        "subreddit_id": subreddit.pk,
        "content": "test_content",
        "score": 100,
        "promoted": False,
        "nsfw": False,
    }
    response: Response = await client.post("/api/v1/post/create", json=data)
    assert response.status_code == status.HTTP_201_CREATED
    response_data: dict[str, str | int | bool | None | dict[str, str]] = response.json()
    assert response_data.pop("subreddit")["id"] == data.pop("subreddit_id")
    del response_data["id"]
    assert response_data == data
