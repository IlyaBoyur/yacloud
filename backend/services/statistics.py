import logging

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import functions

logger = logging.getLogger(__name__)


class RepositoryStatisticsMixin:
    @staticmethod
    async def get_current_time(db: AsyncSession) -> str:
        statement = select(functions.now())
        try:
            result = await db.execute(statement=statement)
            return result.scalar()
        except ConnectionRefusedError as error:
            logger.error(error)
            return ""


class RepositoryStatistics(RepositoryStatisticsMixin):
    pass


statistics_service = RepositoryStatistics()
