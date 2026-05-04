from __future__ import annotations
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Централізоване управління апішкою.

    DATABASE_URL: str
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    ADMIN_BOOTSTRAP_ENABLED: bool = True
    ADMIN_NAME: str = "Asahi Admin"
    ADMIN_EMAIL: str = "yarilslaven@gmail.com"
    ADMIN_LOGIN: str = "asahiadm"
    ADMIN_PASSWORD: str = "654321asahi"
    ADMIN_PHONE_NUMBER: str | None = None

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()
