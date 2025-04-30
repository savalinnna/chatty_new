import pytest
from httpx import AsyncClient
from main import app

@pytest.mark.asyncio
async def test_like_post():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post(
            "/likes/",
            json={"post_id": 1},
            headers={"Authorization": "Bearer 1"}
        )
    assert response.status_code == 201