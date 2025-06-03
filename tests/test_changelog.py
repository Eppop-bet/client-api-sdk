import pytest

from esource_client_api.async_.client import AsyncClient
from conftest import API_URL, TEST_EMAIL, TEST_PASSWORD


@pytest.mark.asyncio
@pytest.mark.integration
async def test_changelog_using_client():
    client = AsyncClient(API_URL, TEST_EMAIL, TEST_PASSWORD)
    await client.login()
    timestamp = "2025-04-02 20:55:18.232"

    response = await client.changelog.list_changelogs(timestamp)

    assert isinstance(response, list)


