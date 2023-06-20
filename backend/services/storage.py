import logging
import os
import shutil
from abc import ABC, abstractmethod
from enum import Enum
from tempfile import SpooledTemporaryFile

from pydantic import BaseModel

from core.config import app_settings

logger = logging.getLogger(__name__)

ERROR_SAVING = "Error while saving {filename}"
ERROR_NO_FILE = "File {name} download error: does not exist"


class FileLoadStatus(str, Enum):
    FINISHED = "finished"
    LOADING = "loading"
    ABORTED = "aborted"


class FileLoadResult(BaseModel):
    status: FileLoadStatus
    path: str | None = None
    file: bytes | None = None


class FileStorage(ABC):
    @abstractmethod
    def upload(self, *args, **kwargs):
        pass

    @abstractmethod
    def download(self, *args, **kwargs):
        pass

    @abstractmethod
    def get_download_stream(self, *args, **kwargs):
        pass


class FileUploadError(RuntimeError):
    pass


class LocalFileStorage(FileStorage):
    def __init__(self, chunk_size: int = 65535):
        self.chunk_size = chunk_size

    @staticmethod
    def parse_path(path: str) -> tuple[str, str, str]:
        path_dir, file = os.path.split(path)
        filename, extension = "", ""
        if file:
            filename, extension = os.path.splitext(file)
        return path_dir, filename, extension

    @staticmethod
    def create_path(path_dir: str, filename: str, extension: str) -> str:
        folder = os.path.join(app_settings.media_root, path_dir)
        os.makedirs(folder, mode=app_settings.storage_mode, exist_ok=True)
        return os.path.join(folder, filename + extension)

    @staticmethod
    def hash_filename(name: str) -> str:
        return name

    async def upload(
        self, path: str, file: SpooledTemporaryFile
    ) -> FileLoadResult:
        path_dir, filename, extension = self.parse_path(path)
        if not filename or not extension:
            filename, extension = os.path.splitext(file.filename)

        if app_settings.storage_hash_filename:
            filename = self.hash_filename(filename)

        result_path = self.create_path(path_dir, filename, extension)
        try:
            with open(result_path, "wb") as new_file:
                shutil.copyfileobj(file.file, new_file)
        except shutil.Error:
            logger.exception(ERROR_SAVING.format(filename=filename))
            return FileLoadResult(status=FileLoadStatus.ABORTED)
        return FileLoadResult(status=FileLoadStatus.FINISHED, path=result_path)

    async def download(self, path: str):
        with open(path, mode="rb") as file:
            for line in file:
                yield line


storage_service = LocalFileStorage()
