import os

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = os.environ.get("PROJECT_NAME")
    SECRET_KEY: str = os.environ.get("SECRET_KEY")
    ALGORITHM: str = os.environ.get("HASHING_ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES")
    DATABASE_URL: str = os.environ.get("DB_URL")

    class Config:
        env_file = ".env"


settings = Settings()
