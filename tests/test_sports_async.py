import pytest

from esource_client_api.async_.sports import Sports
from esource_client_api.models.errors import EsourceCommunicationError, AuthenticationError
from esource_client_api.models.models import Sport
from esource_client_api.async_.session import AsyncSession
from conftest import SPORT_1, SPORT_2, MOCK_BASE_URL, MOCK_LOGIN_SUCCESS_DATA

MOCK_SPORT_LIST_DATA = [SPORT_1, SPORT_2]


@pytest.mark.asyncio
async def test_list_sports_success(httpx_mock):
    httpx_mock.add_response(
        url=f"{MOCK_BASE_URL}/auth/sign-in",
        method="POST",
        json=MOCK_LOGIN_SUCCESS_DATA,
        status_code=200
    )
    httpx_mock.add_response(
        url=f"{MOCK_BASE_URL}/sports",
        method="GET",
        json=MOCK_SPORT_LIST_DATA,
        status_code=200
    )

    async with AsyncSession(base_url=MOCK_BASE_URL) as session:
        await session.login(email="mock@user.com", password="mockpassword")
        sport_resource = Sports(session)
        result_sports = await sport_resource.list_sports()

        assert isinstance(result_sports, list)
        assert len(result_sports) == 2
        assert isinstance(result_sports[0], Sport)
        assert result_sports[0].id == 3
        assert result_sports[1].slug == "lol"


@pytest.mark.asyncio
async def test_get_sport_success(httpx_mock):
    sport_id_to_get = 3

    httpx_mock.add_response(
        url=f"{MOCK_BASE_URL}/auth/sign-in",
        method="POST",
        json=MOCK_LOGIN_SUCCESS_DATA,
        status_code=200
    )
    httpx_mock.add_response(
        url=f"{MOCK_BASE_URL}/sports/{sport_id_to_get}",
        method="GET",
        json=SPORT_1,
        status_code=200
    )

    async with AsyncSession(base_url=MOCK_BASE_URL) as session:
        await session.login(email="mock@user.com", password="mockpassword")
        sport_resource = Sports(session)
        result_sport = await sport_resource.get_sport(3)

        assert isinstance(result_sport, Sport)
        assert result_sport.id == sport_id_to_get
        assert result_sport.name == "Counter-Strike"


@pytest.mark.asyncio
async def test_get_sport_not_found(httpx_mock):
    sport_id_to_get = 999

    httpx_mock.add_response(
        url=f"{MOCK_BASE_URL}/auth/sign-in",
        method="POST",
        json=MOCK_LOGIN_SUCCESS_DATA,
        status_code=200
    )
    httpx_mock.add_response(
        url=f"{MOCK_BASE_URL}/sports/{sport_id_to_get}",
        method="GET",
        text="Not Found",
        status_code=404
    )
    async with AsyncSession(base_url=MOCK_BASE_URL) as session:
        await session.login(email="mock@user.com", password="mockpassword")
        sport_resource = Sports(session)

        with pytest.raises(EsourceCommunicationError) as excinfo:
            await sport_resource.get_sport(sport_id_to_get)

        assert "HTTP Error: 404 Not Found" in str(excinfo.value)


@pytest.mark.asyncio
async def test_list_sports_auth_error(httpx_mock):
    """Test handling of a 401 error when listing sports."""

    httpx_mock.add_response(
        url=f"{MOCK_BASE_URL}/auth/sign-in",
        method="POST",
        json=MOCK_LOGIN_SUCCESS_DATA,
        status_code=200
    )

    httpx_mock.add_response(
        url=f"{MOCK_BASE_URL}/sports",
        method="GET",
        text="Unauthorized",
        status_code=401
    )

    async with AsyncSession(base_url=MOCK_BASE_URL) as session:
        try:
            await session.login(email="mock@user.com", password="mockpassword")
        except AuthenticationError as e:
            pytest.fail(f"Login failed unexpectedly during test setup: {e}")

        sports_resource = Sports(session)

        with pytest.raises(AuthenticationError):
            await sports_resource.list_sports()
