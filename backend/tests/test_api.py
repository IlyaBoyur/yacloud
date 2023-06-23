import pytest
from fastapi import status
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

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
async def auth_user(api_client: AsyncClient) -> dict:
    data = {"email": TEST_USER, "password": TEST_PASSWORD}
    response = await api_client.post(REGISTER_URL, json=data)
    return {**data, **response.json()}


@pytest.fixture
async def auth_client(api_client: AsyncClient, auth_user: dict):
    """Register new user and set JWT token for authorization"""
    query_data = {
        "username": auth_user["email"],
        "password": auth_user["password"],
    }
    response = await api_client.post(LOGIN_URL, data=query_data)
    headers = {"Authorization": f"Bearer {response.json()['access_token']}"}
    api_client.headers = headers
    return api_client


class TestAPIs:
    @pytest.fixture
    async def create_files(self, auth_user: dict, session: AsyncSession):
        id = auth_user["id"]
        UserFileFactory._meta.sqlalchemy_session = session
        return await UserFileFactory.create_batch(3, user_id=id)

    async def test_ping(self, api_client: AsyncClient):
        response = await api_client.get(PING_URL)
        assert response.status_code == status.HTTP_200_OK
        assert "db" in response.json()

    async def test_files(
        self,
        auth_user: dict,
        auth_client: AsyncClient,
        create_files: list[UserFileFactory],
    ):
        response = await auth_client.get(FILES_URL)
        response_json = response.json()
        assert response.status_code == status.HTTP_200_OK
        assert response_json["account_id"] == auth_user["id"]
        assert len(response_json["files"]) == len(create_files)

    async def test_files_anonymous(self, api_client: AsyncClient):
        response = await api_client.get(FILES_URL)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    async def test_upload_anonymous(self, api_client: AsyncClient):
        response = await api_client.post(UPLOAD_URL)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    async def test_download_anonymous(self, api_client: AsyncClient):
        response = await api_client.get(DOWNLOAD_URL)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
