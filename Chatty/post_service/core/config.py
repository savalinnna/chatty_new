from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # ---------- DATABASE ----------
    post_db_url: str

    # ---------- S3 / MinIO ----------
    s3_endpoint: str
    s3_bucket_name: str
    s3_access_key: str
    s3_secret_key: str

    # ---------- JWT ----------
    jwt_secret: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # ---------- SERVICE URLs ----------
    auth_service_url: str

    # ---------- DEBUG ----------
    debug: bool = False

    # ---------- CONFIG ----------
    model_config = SettingsConfigDict(
        env_file="../../.env",  # только если ты на 100% уверен в относительном пути
        env_file_encoding="utf-8",
        extra="forbid"
    )

    @property
    def async_database_url(self) -> str:
        return self.post_db_url


settings = Settings()

