from typing import Any

from fastapi import APIRouter, Body, Depends, UploadFile, status
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import StreamingResponse

from db import get_session
from models import User
from schemas import UserFileCreate, UserFileList, UserFileRead
from services import (
    FileLoadStatus,
    current_user,
    storage_service,
    user_file_service,
)
from utils import set_content_disposition

router = APIRouter()


@router.get("/", response_model=UserFileList)
async def files(
    db: AsyncSession = Depends(get_session),
    skip: int = 0,
    limit: int = 100,
    user: User = Depends(current_user),
) -> UserFileList:
    """Retrieve list of file infos."""

    response = await user_file_service.get_multi(
        db, filter=dict(user_id=user.id), skip=skip, limit=limit
    )
    return UserFileList(account_id=user.id, files=response)


@router.post(
    "/upload", response_model=UserFileRead, status_code=status.HTTP_201_CREATED
)
async def upload(
    *,
    db: AsyncSession = Depends(get_session),
    user: User = Depends(current_user),
    file: UploadFile,
    path: str = Body(),
) -> UserFileRead:
    """Upload file to user`s storage."""

    result = await storage_service.upload(
        path=path, file=file.file, name=file.filename
    )
    if result.status != FileLoadStatus.FINISHED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"During {file.filename} upload error occurred.",
        )
    object_in = UserFileCreate(
        user_id=user.id,
        name=result.path.split("/")[-1],
        path=result.path,
        size=file.size,
        is_downloadable=True,
    )
    filter = object_in.dict()
    [filter.pop(key) for key in ["size", "user_id"]]
    count = await user_file_service.count(db, filter=filter)
    if count > 0:
        await user_file_service.delete(db=db, filter=filter)
    new_file = await user_file_service.create(db, object_in=object_in)
    return new_file


@router.get("/download", status_code=status.HTTP_200_OK)
async def download(
    db: AsyncSession = Depends(get_session),
    user: User = Depends(current_user),
    path: str = "",
) -> Any:
    """Download file."""

    file = await user_file_service.get_by_path(db, path=path, user_id=user.id)
    if file is not None:
        stream = storage_service.get_download_stream(file.path)
        headers = {}
        set_content_disposition(headers, file.name)
        return StreamingResponse(
            content=stream,
            media_type="application/octet-stream",
            headers=headers,
        )
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, detail="File not found."
    )
