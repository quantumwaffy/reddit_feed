import pytest
from fastapi import status
from httpx import AsyncClient, Response


@pytest.mark.anyio
async def test_create_subreddit(client: AsyncClient):
    data: dict[str, str] = {"name": "subreddit_test"}
    response: Response = await client.post("/api/v1/subreddit/create", json=data)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["name"] == data["name"]
