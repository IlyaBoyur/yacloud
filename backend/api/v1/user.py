import logging

from fastapi import APIRouter

from schemas import UserCreate, UserRead
from services.user import fastapi_users, jwt_backend

router = APIRouter()
logger = logging.getLogger(__name__)


router.include_router(fastapi_users.get_register_router(UserRead, UserCreate))
router.include_router(fastapi_users.get_auth_router(jwt_backend))
