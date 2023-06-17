import logging
import time

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import functions

from db import get_session
from schemas.status import Status, StatusError

router = APIRouter()
logger = logging.getLogger(__name__)

DB_CONNECTION_ERROR = "Database connection error occurred."


@router.get("/ping", response_model=Status)
async def ping(
    *, db: AsyncSession = Depends(get_session)
) -> Status | StatusError:
    """Get service status"""
    try:
        start = time.perf_counter()
        await db.execute(statement=select(functions.now()))
        elapsed = time.perf_counter() - start
        return Status(db=elapsed)
    except ConnectionError as error:
        logger.exception(error)
        return StatusError(detail=DB_CONNECTION_ERROR)
