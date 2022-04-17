from pydantic import BaseSettings, SecretStr

from pathlib import Path

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
    TEST_DB_USERNAME: str
    TEST_DB_PASSWORD: SecretStr
    TEST_DB_HOST: str
    TEST_DB_PORT: int
    TEST_DB_NAME: str

    SECRET_KEY: str
    SECRET_ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30


    class Config:
        env_file = str(BASE_DIR / ".env")
        env_file_encoding = "utf-8"



settings = Settings()
