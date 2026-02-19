"""
Application configuration from environment variables.
"""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Load from .env. Use env vars in production."""

    # App
    APP_NAME: str = "School Management API"
    DEBUG: bool = False

    # Database
    DATABASE_URL: str = "postgresql://drivergo:drivergopass@127.0.0.1:5432/drivergo_db"

    # Auth (never commit real secrets; use .env)
    SECRET_KEY: str = "change-me-in-production-use-env"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # CORS
    CORS_ORIGINS: str = "*"  # e.g. "http://localhost:3000,https://mysite.com"

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
