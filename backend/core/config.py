from logging import config as logging_config

from pydantic import BaseSettings, HttpUrl, PostgresDsn

from core.logger import LOGGING

logging_config.dictConfig(LOGGING)


class AppSettings(BaseSettings):
    project_name: str = ""
    project_host: str | HttpUrl = "localhost"
    project_port: int = 8080
    project_db: PostgresDsn = (
        "postgresql+asyncpg://postgres:postgres@localhost:5432/postgres"
    )
    jwt_secret_key: str
    jwt_lifetime_secs: int = 3600
    media_root: str = "media"
    storage_hash_filename: bool = False
    storage_mode: int = 0o744
    storage_chunk_size: int = 65535

    class Config:
        env_file = ".env"


app_settings = AppSettings()
