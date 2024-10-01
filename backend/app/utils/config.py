from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """
    Environment variables automatic parser.
    """

    APP_NAME: Optional[str] = None
    APP_VERSION: Optional[str] = None
    PORT: Optional[int] = 8000
    APP_HOST: Optional[str] = None
    MONGO_DB_URI: Optional[str] = None
    MONGO_DBNAME: Optional[str] = None
    PYTHON_ENV: Optional[str] = None
    DOCS_ENABLED: Optional[bool] = False
    DATABASE_HOSTNAME: Optional[str] = None
    DATABASE_PORT: Optional[int] = 5432
    DATABASE_PASSWORD: Optional[str] = None
    DATABASE_NAME: Optional[str] = None
    DATABASE_USERNAME: Optional[str] = None
    POSTGRES_DB: Optional[str] = None
    POSTGRES_PASSWORD: Optional[str] = None

    class Config:
        env_file = "../.env"


configs = Settings()
