import factory

from db import async_session, get_session
from models import User, UserFile


class AsyncModelFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        abstract = True

    @classmethod
    def _save(cls, model_class, session, args, kwargs):
        """Add asynchronous creation support"""

        async def create_coro(*args, **kwargs):
            db_object = model_class(*args, **kwargs)
            async with session() as s:
                s.add(db_object)
                await s.commit()
                await s.refresh(db_object)
            return db_object

        return create_coro(*args, **kwargs)

    @classmethod
    async def create_batch(cls, size, **kwargs):
        model_coros = super().create_batch(size, **kwargs)
        return [await model for model in model_coros]


class UserFactory(AsyncModelFactory):
    id = factory.Faker("uuid4")
    email = factory.Faker("email")
    hashed_password = factory.Faker("password")
    is_active = factory.Faker("boolean")
    is_superuser = factory.Faker("boolean")
    is_verified = factory.Faker("boolean")
    created_at = factory.Faker("date_time")

    class Meta:
        model = User
        sqlalchemy_session = async_session


class UserFileFactory(AsyncModelFactory):
    id = factory.Faker("uuid4")
    user_id = factory.SubFactory(UserFactory)
    name = factory.LazyAttribute(lambda obj: obj.path.split("/")[-1])
    created_at = factory.Faker("date_time")
    path = factory.Faker("file_path", depth=3, absolute=False)
    size = factory.Faker("random_int", min=1)

    class Meta:
        model = UserFile
        sqlalchemy_session = async_session
