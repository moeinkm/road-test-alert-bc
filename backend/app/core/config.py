from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    ENVIRONMENT: str

    # Backend settings
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    ALGORITHM: str
    API_V1_STR: str = '/api/v1'
    DATABASE_URL: str
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

    # Script configuration
    CHECK_AVAILABILITY_INTERVAL: int  # Check for availability within this many days

    # Google API User ID (generally 'me' for the authorized user)
    GMAIL_USER_ID: str

    class Config:
        env_file = ".env"


# Load settings once
settings = Settings()
