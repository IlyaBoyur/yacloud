from logging import config as logging_config

from pydantic import BaseSettings, HttpUrl, PostgresDsn

from core.logger import LOGGING

logging_config.dictConfig(LOGGING)


class AppSettings(BaseSettings):
    project_host: str | HttpUrl = "localhost"
    project_port: int = 8080
    project_db: PostgresDsn = "postgresql+asyncpg://postgres:postgres@localhost:5432/postgres"

    class Config:
        env_file = ".env"


app_settings = AppSettings()
