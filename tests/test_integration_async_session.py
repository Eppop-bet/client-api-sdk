import pytest
from datetime import datetime, timezone

from esource_client_api.async_.session import AsyncSession, AuthenticationError, EsourceCommunicationError
from conftest import API_URL, TEST_EMAIL, TEST_PASSWORD


@pytest.mark.asyncio
@pytest.mark.integration
async def test_real_login_sets_token_and_expiration():
    """Tests successful async login sets token and expiration time."""
    async with AsyncSession(API_URL) as session:
        try:
            await session.login(email=TEST_EMAIL, password=TEST_PASSWORD)

            assert session.token is not None
            assert session._token_expiration_time is not None
            assert isinstance(session._token_expiration_time, datetime)
            assert session._token_expiration_time > datetime.now(timezone.utc)
            assert "Authorization" in session.client.headers
            assert session.client.headers["Authorization"] == session.token

        except (AuthenticationError, EsourceCommunicationError) as e:
            pytest.fail(f"Login failed unexpectedly during test: {e}")


@pytest.mark.asyncio
@pytest.mark.integration
async def test_login_failure_raises_exception():
    """Tests that async login with invalid credentials raises AuthenticationError."""
    async with AsyncSession(API_URL) as session:
        with pytest.raises(AuthenticationError):
            await session.login(email=TEST_EMAIL, password="wrongpassword")

        assert session.token is None
        assert "Authorization" not in session.client.headers
