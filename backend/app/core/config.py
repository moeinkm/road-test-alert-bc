from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    ALGORITHM: str
    API_V1_STR: str = '/api/v1'
    DATABASE_URL: str
    PROJECT_NAME: str
    SECRET_KEY: str

    class Config:
        env_file = ".env"


# Load settings once
settings = Settings()
