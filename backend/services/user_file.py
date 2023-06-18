from models import UserFile as UserFileModel
from schemas import UserFileCreate

from .base import RepositoryDB


class RepositoryUserFile(RepositoryDB[UserFileModel, UserFileCreate, None]):
    pass


user_file_service = RepositoryUserFile(UserFileModel)
