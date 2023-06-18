import logging
import os
import shutil
from enum import Enum
from tempfile import SpooledTemporaryFile

from pydantic import BaseModel

from core.config import app_settings

logger = logging.getLogger(__name__)

ERROR_NO_FILE = "File {name} download error: does not exist"


class FileLoadStatus(str, Enum):
    FINISHED = "finished"
    LOADING = "loading"
    ABORTED = "aborted"


class FileLoadResult(BaseModel):
    status: FileLoadStatus
    path: str | None = None
    file: bytes | None = None


class FileStorage:
    def upload(self, *args, **kwargs):
        raise NotImplementedError

    def download(self, *args, **kwargs):
        raise NotImplementedError


class FileUploadError(RuntimeError):
    pass


class LocalFileStorage(FileStorage):
    @staticmethod
    def parse_path(path: str) -> tuple[str, str, str]:
        path_dir, file = os.path.split(path)
        filename, extension = "", ""
        if file:
            filename, extension = os.path.splitext(file)
        return path_dir, filename, extension

    @staticmethod
    def create_path(path_dir: str, filename: str, extension: str) -> str:
        root = app_settings.media_root
        if not os.path.isdir(root):
            os.mkdir(root)
        folder = os.path.join(root, path_dir)
        if not os.path.isdir(folder):
            os.mkdir(folder)
        return os.path.join(folder, filename + extension)

    @staticmethod
    def hash_filename(name: str) -> str:
        return name

    async def upload(
        self, path: str, file: SpooledTemporaryFile
    ) -> FileLoadResult:
        path_dir, pathfilename, pathextension = self.parse_path(path)
        if pathfilename and pathextension:
            filename = pathfilename
            extension = pathextension
        else:
            filename, extension = os.path.splitext(file.filename)

        if app_settings.storage_hash_filename:
            filename = self.hash_filename(filename)

        result_path = self.create_path(path_dir, filename, extension)
        try:
            with open(result_path, "wb") as f:
                shutil.copyfileobj(file.file, f)
        except Exception as error:
            logger.exception(error)
            return FileLoadResult(status=FileLoadStatus.ABORTED)
        return FileLoadResult(status=FileLoadStatus.FINISHED, path=result_path)


storage_service = LocalFileStorage()
