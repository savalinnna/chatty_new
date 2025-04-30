from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from db.session import get_session

security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> int:
    token = credentials.credentials
    # Здесь должна быть реальная проверка токена (например, через Auth service)
    # Временно эмулируем: просто возвращаем user_id из токена как int, если он числовой
    if token.isdigit():
        return int(token)
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication credentials",
    )

async def get_db() -> AsyncSession:
    async for session in get_session():
        yield session