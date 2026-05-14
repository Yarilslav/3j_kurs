from __future__ import annotations

from sqlalchemy.engine import make_url

from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Централізоване управління апішкою.

    ENVIRONMENT: str = "development"
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8000
    PORT: int | None = None
    APP_RELOAD: bool = False
    DATABASE_URL: str
    POSTGRES_DB: str | None = None
    POSTGRES_USER: str | None = None
    POSTGRES_PASSWORD: str | None = None
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    ADMIN_BOOTSTRAP_ENABLED: bool = True
    ADMIN_NAME: str = "Asahi Admin"
    ADMIN_EMAIL: str = "yarilslaven@gmail.com"
    ADMIN_LOGIN: str = "asahiadm"
    ADMIN_PASSWORD: str = "654321asahi"
    ADMIN_PHONE_NUMBER: str | None = None
    FRONTEND_CORS_ORIGINS: str = "http://localhost:5173,http://127.0.0.1:5173"

    @property
    def cors_origins(self) -> list[str]:
        return [origin.strip() for origin in self.FRONTEND_CORS_ORIGINS.split(",") if origin.strip()]

    @property
    def app_port(self) -> int:
        return self.PORT or self.APP_PORT

    @model_validator(mode="after")
    def normalize_database_settings(self) -> "Settings":
        database_url = self.DATABASE_URL.replace("postgres://", "postgresql://", 1)
        url = make_url(database_url)

        if url.drivername == "postgresql":
            url = url.set(drivername="postgresql+psycopg_async")
        elif url.drivername in {"postgresql+psycopg", "postgresql+psycopg2"}:
            url = url.set(drivername="postgresql+psycopg_async")

        self.DATABASE_URL = str(url)
        self.POSTGRES_DB = self.POSTGRES_DB or url.database
        self.POSTGRES_USER = self.POSTGRES_USER or url.username
        self.POSTGRES_PASSWORD = self.POSTGRES_PASSWORD or url.password
        return self

    @model_validator(mode="after")
    def validate_production_settings(self) -> "Settings":
        if self.ENVIRONMENT.lower() not in {"production", "prod"}:
            return self

        insecure_secret_keys = {
            "dev-secret-key-change-me-please-32-bytes",
            "test-secret-key-with-at-least-32-bytes",
        }
        if self.SECRET_KEY in insecure_secret_keys or len(self.SECRET_KEY) < 32:
            raise ValueError("SECRET_KEY must be changed to a strong 32+ character value in production")

        if self.ADMIN_BOOTSTRAP_ENABLED and self.ADMIN_PASSWORD == "654321asahi":
            raise ValueError("ADMIN_PASSWORD must be changed or ADMIN_BOOTSTRAP_ENABLED disabled in production")

        return self

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()
