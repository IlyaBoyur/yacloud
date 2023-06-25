import logging

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db import get_session
from schemas.status import Status, StatusError
from services import Cache, get_cache, statistics_service
from utils import elapse

router = APIRouter()
logger = logging.getLogger(__name__)

DB_CONNECTION_ERROR = "Database connection error occurred."


@router.get("/ping", response_model=Status)
async def ping(
    *,
    db: AsyncSession = Depends(get_session),
    cache: Cache = Depends(get_cache)
) -> Status | StatusError:
    """Get service status"""
    try:
        status = Status(
            db=await elapse(statistics_service.get_current_time(db)),
            cache=await elapse(cache.ping()),
        )
        return status
    except ConnectionError:
        logger.exception(DB_CONNECTION_ERROR)
        return StatusError(detail=DB_CONNECTION_ERROR)
