from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from db.session import get_db
from core.config import settings
import models
import httpx

security = HTTPBearer()

class AuthClient:
    def __init__(self, base_url: str):
        self.base_url = base_url

    async def verify_token(self, token: str):
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/internal/verify-token",
                headers={"Authorization": f"Bearer {token}"}
            )
            if response.status_code != 200:
                raise HTTPException(status_code=401, detail="Invalid token")
            return response.json()

auth_client = AuthClient(base_url=settings.AUTH_SERVICE_URL)

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
):
    token = credentials.credentials

    try:
        user_info = await auth_client.verify_token(token)
        user_id = int(user_info["id"])
    except (KeyError, ValueError, JWTError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )

    result = await db.execute(select(models.User).where(models.User.id == user_id))
    user = result.scalar_one_or_none()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return user

