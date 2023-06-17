import logging

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db import get_session
from schemas.status import Status

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/ping", response_model=Status)
async def ping(*, db: AsyncSession = Depends(get_session)) -> Status:
    """Get service status"""
    return {"message": "test"}
