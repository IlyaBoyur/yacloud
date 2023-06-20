from sqlalchemy.ext.asyncio import AsyncSession

from models import UserFile as UserFileModel
from schemas import UserFileCreate

from .base import ModelType, RepositoryDB


class RepositoryUserFile(RepositoryDB[UserFileModel, UserFileCreate, None]):
    async def get_by_path(
        self, db: AsyncSession, path: str, user_id: str
    ) -> ModelType | None:
        if (
            record := await self.get(db, id=path)
        ) is not None and record.user_id == user_id:
            return record
        if records := await self.get_multi(
            db, filter={"path": path, "user_id": user_id}
        ):
            return records[0]


user_file_service = RepositoryUserFile(UserFileModel)
