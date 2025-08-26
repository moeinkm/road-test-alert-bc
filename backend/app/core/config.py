import os
from pydantic_settings import BaseSettings

ENV_FILE_PATH = ".env"


class Settings(BaseSettings):
    ENVIRONMENT: str

    # Backend settings
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    ALGORITHM: str
    API_V1_STR: str = '/api/v1'
    DATABASE_URL: str
    DATABASE_USER: str
    DATABASE_PASSWORD: str
    DATABASE_NAME: str
    TEST_DATABASE_URL: str
    PROJECT_NAME: str
    SECRET_KEY: str

    # Authentication credentials for login and authorization
    USER_LAST_NAME: str
    USER_LICENSE_NUMBER: str
    USER_KEYWORD: str

    # Gmail configuration
    SENDER_EMAIL: str
    FROM_HEADER: str
    TO_EMAILS: str
    MAIL_SUBJECT: str
    SMTP_SERVER: str
    SMTP_PORT: int

    # Google Account credentials
    APP_PASSWORD: str

    # Google API User ID (generally 'me' for the authorized user)
    GMAIL_USER_ID: str

    # ICBC URLs
    ICBC_LOGIN_URL: str
    ICBC_APPOINTMENT_URL: str
    ICBC_TEST_CENTERS_LOCATION_URL: str

    class Config:
        env_file = ENV_FILE_PATH


# Load settings once
settings = Settings()
