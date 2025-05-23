#from pydantic_settings import BaseSettings

#class Settings(BaseSettings):
    #url_auth_service: str = "http://auth-service:8000"
    #url_post_service: str = "http://post-service:8000"
    #subscription_db_url: str = "postgresql+asyncpg://user:password@localhost:5432/subscriptions"
    #redis_url: str = "redis://localhost:6379"
    #jwt_secret: str = "your-secret-key"
    #debug: bool = True

    #class Config:
        #env_file = ".env"
        #env_file_encoding = "utf-8"

#settings = Settings()

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv
from pathlib import Path

# Путь до корня проекта
BASE_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(dotenv_path=BASE_DIR / ".env")

class Settings(BaseSettings):
    # ---------- DATABASE ----------
    subscription_db_url: str = Field(alias="SUBSCRIPTION_DB_URL")

    # ---------- RABBITMQ ----------
    rabbitmq_host: str = Field(alias="RABBITMQ_HOST")
    rabbitmq_port: int = Field(alias="RABBITMQ_PORT")

    # ---------- SERVICES ----------
    url_auth_service: str = Field(alias="AUTH_SERVICE_URL")
    url_post_service: str = Field(alias="POST_SERVICE_URL")

    # ---------- JWT ----------
    jwt_secret: str = Field(alias="JWT_SECRET")
    jwt_algorithm: str = Field(default="HS256", alias="JWT_ALGORITHM")
    jwt_access_token_expire_minutes: int = Field(default=30, alias="JWT_ACCESS_TOKEN_EXPIRE_MINUTES")

    # ---------- REDIS ----------
    redis_host: str = Field(alias="REDIS_HOST")
    redis_port: int = Field(alias="REDIS_PORT")

    # ---------- DEBUG ----------
    debug: bool = Field(default=False, alias="DEBUG")

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        extra="forbid"
    )

    @property
    def async_database_url(self) -> str:
        return self.subscription_db_url

    @property
    def redis_url(self) -> str:
        return f"redis://{self.redis_host}:{self.redis_port}/0"

settings = Settings()