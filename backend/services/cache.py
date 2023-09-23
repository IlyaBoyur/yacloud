import logging
from abc import ABC, abstractmethod
from typing import Any

from redis import Redis

from core.config import app_settings

logger = logging.getLogger(__name__)


class Cache(ABC):
    @abstractmethod
    async def get(self, *args, **kwargs):
        pass

    @abstractmethod
    async def set(self, *args, **kwargs):
        pass

    @abstractmethod
    async def ping(self, *args, **kwargs):
        pass


class RedisCache(Cache):
    def __init__(self, url: str, expire_secs: int = 60):
        self.url = url
        self.connection = None
        self.expire_secs = expire_secs

    def __enter__(self) -> "RedisCache":
        """Make a database connection and return it."""
        self.connection = Redis.from_url(url=self.url, decode_responses=True)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Make sure the db connection gets closed."""
        self.connection.close()
        self.connection = None

    async def get(self, key: str) -> Any:
        if self.connection.exists(key):
            logger.info("CACHE GET %s", key)
            return self.connection.get(key)
        return None

    async def set(self, key: str, value: str, secs: int | None = None):
        if not self.connection.exists(key):
            try:
                data = value.encode("utf-8")
            except UnicodeEncodeError:
                logger.exception("CACHE SET ERROR")
            else:
                logger.info("CACHE SET %s", data)
                self.connection.setex(key, secs or self.expire_secs, data)

    async def ping(self):
        return self.connection.ping()


async def get_cache() -> Cache:
    with RedisCache(
        url=app_settings.cache_url,
        expire_secs=app_settings.cache_expire_secs,
    ) as cache:
        yield cache
