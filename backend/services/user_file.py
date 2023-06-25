import logging

from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from models import UserFile as UserFileModel
from schemas import UserFileCreate, UserFileRead

from .base import RepositoryDB
from .cache import Cache

logger = logging.getLogger(__name__)


class RepositoryUserFile(RepositoryDB[UserFileModel, UserFileCreate, None]):
    async def get_by_path(
        self, db: AsyncSession, path: str, user_id: str
    ) -> UserFileModel | None:
        if (
            record := await self.get(db, id=path)
        ) is not None and record.user_id == user_id:
            return record
        if records := await self.get_multi(
            db, filter={"path": path, "user_id": user_id}
        ):
            return records[0]

    @staticmethod
    async def get_from_cache(cache: Cache, key: str) -> UserFileRead | None:
        try:
            value = await cache.get(key=key)
            if value is not None:
                return UserFileRead.parse_raw(value)
        except ValidationError:
            logger.exception(f"Couldn't get file from cache")
        return None

    @staticmethod
    async def set_in_cache(cache: Cache, key: str, file: UserFileRead) -> None:
        await cache.set(key=key, value=file.json())


user_file_service = RepositoryUserFile(UserFileModel)
