from logging import config as logging_config

from pydantic import BaseSettings, HttpUrl, PostgresDsn, RedisDsn

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
    storage_mode: int = 0o777
    storage_chunk_size: int = 65535
    cache_url: RedisDsn = "redis://localhost:6379/0"
    cache_expire_secs: int = 60

    class Config:
        env_file = ".env"


app_settings = AppSettings()
