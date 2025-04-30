import pytest
from httpx import AsyncClient
from fastapi import status
from app.main import app
from app.clients import AuthClient

@pytest.mark.asyncio
async def test_subscribe_flow():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # заголовок авторизации
        headers = {"Authorization": "Bearer test-token"}

        # get_current_user через зависимость
        app.dependency_overrides = {
            # Импорт actual deps.get_current_user
            # и заменa на lambda: {"id": 1}
        }

        # Подписка
        response = await ac.post("/subscriptions/subscribe/2", headers=headers)
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["detail"] == "Subscribed to user 2"

        # Получение подписок
        response = await ac.get("/subscriptions/subscriptions", headers=headers)
        assert response.status_code == status.HTTP_200_OK
        assert 2 in response.json()["subscriptions"]

        # Отписка
        response = await ac.delete("/subscriptions/unsubscribe/2", headers=headers)
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["detail"] == "Unsubscribed from user 2"

        # Проверяем, что отписались
        response = await ac.get("/subscriptions/subscriptions", headers=headers)
        assert 2 not in response.json()["subscriptions"]

