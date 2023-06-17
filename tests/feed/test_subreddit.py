from fastapi import status
from httpx import Response
from starlette.testclient import TestClient


def test_create_subreddit(test_app: TestClient):
    data: dict[str, str] = {"name": "subreddit_test"}
    response: Response = test_app.post("/api/v1/subreddit/create", json=data)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["name"] == data["name"]
