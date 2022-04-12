from pydantic import BaseSettings, SecretStr
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    PROJECT_NAME: str = "Cafe Search"
    PROJECT_VERSION: str = "1.0.0"

    DB_USERNAME: str
    DB_PASSWORD: SecretStr
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str

    SECRET_KEY: str
    SECRET_ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30

    class Config:
        env_file = str(BASE_DIR / ".env")
        env_file_encoding = "utf-8"


class TestSettings(BaseSettings):
    DB_USERNAME: str
    DB_PASSWORD: SecretStr
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str

    TEST_USER_EMAIL: str
    TEST_USER_PASSWORD: str
    TEST_ADMIN_EMAIL: str
    TEST_SECOND_USER_EMAIL: str

    SECRET_KEY: str = "secret"
    SECRET_ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30

    class Config:
        env_file = str(BASE_DIR / ".env")
        env_file_encoding = "utf-8"


def get_settings():
    if os.getenv("APP_ENV", "DEVELOP") == "TEST":
        return TestSettings()
    return Settings()


settings = get_settings()
