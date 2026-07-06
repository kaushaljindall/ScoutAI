from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    PROJECT_NAME: str = "ScoutAI"
    ENVIRONMENT: str = "development"
    API_V1_STR: str = "/api/v1"

    # Security
    SECRET_KEY: str
    JWT_SECRET: str
    JWT_REFRESH_SECRET: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # Database - MongoDB
    MONGODB_URI: str = "mongodb://localhost:27017"
    MONGODB_DB_NAME: str = "scoutai"

    # Database - PostgreSQL
    POSTGRES_URI: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/scoutai"

    # Frontend URL
    FRONTEND_URL: str = "http://localhost:3000"

    # AI Config
    GEMINI_API_KEY: str = ""

    model_config = {
        "env_file": ".env",
        "case_sensitive": True,
        "extra": "ignore",   # ← ignores any unknown keys in .env (e.g. old DATABASE_URL)
    }


settings = Settings()
