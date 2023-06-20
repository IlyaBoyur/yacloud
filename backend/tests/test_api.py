import pytest
from fastapi import status
from httpx import AsyncClient

from main import app

from .factories import UserFactory, UserFileFactory

pytestmark = pytest.mark.anyio


PING_URL = app.url_path_for("ping")
FILES_URL = app.url_path_for("files")
UPLOAD_URL = app.url_path_for("upload")
DOWNLOAD_URL = app.url_path_for("download")
LOGIN_URL = "/api/v1/login"
REGISTER_URL = "/api/v1/register"
TEST_USER = "testuser@test.com"
TEST_PASSWORD = "password"


@pytest.fixture
async def auth_client(api_client: AsyncClient):
    """Register new user and set JWT token for authorization"""
    await api_client.post(
        REGISTER_URL,
        json={"email": TEST_USER, "password": TEST_PASSWORD},
    )
    response = await api_client.post(
        LOGIN_URL, data={"username": TEST_USER, "password": TEST_PASSWORD}
    )
    headers = {"Authorization": f"Bearer {response.json()['access_token']}"}
    api_client.headers = headers
    return api_client


class TestAPIs:
    @pytest.fixture
    async def create_files(self):
        users = [await UserFactory() for _ in range(3)]
        files = [await UserFileFactory(user_id=user.id) for user in users]
        return files

    async def test_ping(self, api_client: AsyncClient):
        response = await api_client.get(PING_URL)
        assert response.status_code == status.HTTP_200_OK
        assert "db" in response.json()

    async def test_files(
        self, auth_client: AsyncClient, create_files: list[UserFileFactory]
    ):
        response = await auth_client.get(FILES_URL)
        assert response.status_code == status.HTTP_200_OK

    async def test_files_anonymous(self, api_client: AsyncClient):
        response = await api_client.get(FILES_URL)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    async def test_upload_anonymous(self, api_client: AsyncClient):
        response = await api_client.post(UPLOAD_URL)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    async def test_download_anonymous(self, api_client: AsyncClient):
        response = await api_client.get(DOWNLOAD_URL)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
