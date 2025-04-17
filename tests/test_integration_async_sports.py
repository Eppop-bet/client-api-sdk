import pytest

from esource_client_api.async_.session import AsyncSession
from conftest import API_URL, TEST_EMAIL, TEST_PASSWORD
from esource_client_api.async_.sports import Sports
from esource_client_api.models.models import Sport


@pytest.mark.asyncio
@pytest.mark.integration
async def test_get_all_sports():
    session = AsyncSession(API_URL, TEST_EMAIL, TEST_PASSWORD)
    await session.login()
    sports = Sports(session)

    response = await sports.list_sports()

    assert isinstance(response, list)
    assert all(isinstance(sport, Sport) for sport in response)


@pytest.mark.asyncio
@pytest.mark.integration
async def test_get_sport_by_id():
    session = AsyncSession(API_URL, TEST_EMAIL, TEST_PASSWORD)
    await session.login()
    sports = Sports(session)

    response = await sports.get_sport(3)

    assert response.id == 3
    assert response.slug == "cs-go"
    assert response.name == "Counter-Strike"
