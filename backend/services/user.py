import logging
import uuid

from fastapi import Depends, Request
from fastapi_users import (
    BaseUserManager,
    FastAPIUsers,
    UUIDIDMixin,
    models,
    schemas,
)
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    JWTStrategy,
)
from fastapi_users.db import SQLAlchemyUserDatabase
from fastapi_users.exceptions import InvalidPasswordException
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import app_settings
from db import get_session
from models import User

logger = logging.getLogger(__name__)


async def get_user_service(db: AsyncSession = Depends(get_session)):
    yield SQLAlchemyUserDatabase(db, User)


class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret = app_settings.jwt_secret_key
    verification_token_secret = app_settings.jwt_secret_key

    async def on_after_register(
        self, user: User, request: Request | None = None
    ):
        logger.info(f"User %s has signed up.".format(user.id))

    async def on_after_login(
        self,
        user: models.UP,
        request: Request | None = None,
        response: Request | None = None,
    ) -> None:
        logger.info(f"User %s has logged in.".format(user.id))

    async def validate_password(
        self, password: str, user: schemas.UC | models.UP
    ) -> None:
        if len(password) < 8:
            raise InvalidPasswordException(
                "Password should be at least 8 characters"
            )
        if user.email in password:
            raise InvalidPasswordException(
                "Password should not contain e-mail"
            )


async def get_user_manager(user_db=Depends(get_user_service)):
    yield UserManager(user_db)


bearer_transport = BearerTransport(tokenUrl="/api/v1/login")


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(
        secret=app_settings.jwt_secret_key,
        lifetime_seconds=app_settings.jwt_lifetime_secs,
    )


jwt_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)


fastapi_users = FastAPIUsers[User, uuid.UUID](
    get_user_manager=get_user_manager,
    auth_backends=[jwt_backend],
)
