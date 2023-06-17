from fastapi import APIRouter

from .statistics import router as statistics_router
from .user import router as user_router

api_router = APIRouter()

api_router.include_router(statistics_router)
api_router.include_router(user_router)
