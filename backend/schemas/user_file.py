import uuid
from datetime import datetime

from fastapi_users import schemas
from pydantic import BaseModel


class UserFileInDB(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    name: str
    created_at: datetime
    path: str
    size: int
    is_downloadable: bool

    class Config:
        orm_mode = True


class UserFileRead(UserFileInDB):
    pass


class UserFileCreate(BaseModel):
    user_id: uuid.UUID
    name: str
    path: str
    size: int
    is_downloadable: bool | None = False


class UserFileUpdate(schemas.BaseUserUpdate):
    name: str
    path: str
    size: int
    is_downloadable: bool | None = False


class UserFileList(BaseModel):
    account_id: uuid.UUID
    files: list[UserFileRead]
