from typing import Any

from fastapi import APIRouter, Body, Depends, UploadFile, status
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import StreamingResponse

from db import get_session
from models import User
from schemas import UserFileCreate, UserFileList, UserFileRead
from services import (
    Cache,
    FileLoadStatus,
    current_user,
    get_cache,
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
        db, filter={"user_id": user.id}, skip=skip, limit=limit
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
    return await user_file_service.create(db, object_in=object_in)


@router.get("/download", status_code=status.HTTP_200_OK)
async def download(
    db: AsyncSession = Depends(get_session),
    user: User = Depends(current_user),
    path: str = "",
    cache: Cache = Depends(get_cache),
) -> Any:
    """Download file."""
    file = await user_file_service.get_from_cache(cache, key=path)
    if file is None:
        file = await user_file_service.get_by_path(
            db, path=path, user_id=user.id
        )
    if file is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="File not found."
        )
    await user_file_service.set_in_cache(
        cache, str(file.id), UserFileRead.from_orm(file)
    )
    stream = storage_service.get_download_stream(file.path)
    headers = {}
    set_content_disposition(headers, file.name)
    return StreamingResponse(
        content=stream,
        media_type="application/octet-stream",
        headers=headers,
    )
