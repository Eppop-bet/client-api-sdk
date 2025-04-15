import httpx
import pytest
from datetime import datetime, timezone

from models.errors import AuthenticationError, EsourceCommunicationError
from async_.players import Players
from async_.session import AsyncSession
from models.models import Player
from conftest import PLAYER_1, PLAYER_2, MOCK_BASE_URL, MOCK_LOGIN_SUCCESS_DATA

MOCK_PLAYER_LIST_DATA = [PLAYER_1, PLAYER_2]


@pytest.mark.asyncio
async def test_list_players_success(httpx_mock):
    """Test successfully listing players with mock data."""

    httpx_mock.add_response(
        url=f"{MOCK_BASE_URL}/auth/sign-in",
        method="POST",
        json=MOCK_LOGIN_SUCCESS_DATA,
        status_code=200
    )

    expected_params = {"skip": "10", "take": "5", "search": "Mock", "orderBy": "name", "orderDir": "desc"}
    expected_url = httpx.URL(f"{MOCK_BASE_URL}/players", params=expected_params)
    httpx_mock.add_response(
        url=expected_url,
        method="GET",
        json=MOCK_PLAYER_LIST_DATA,
        status_code=200
    )

    async with AsyncSession(base_url=MOCK_BASE_URL) as session:
        await session.login(email="mock@user.com", password="mockpassword")
        players_resource = Players(session)
        result_players = await players_resource.list_players(skip=10, take=5, search="Mock", order_by={"name": "desc"})

        assert isinstance(result_players, list)
        assert len(result_players) == 2
        assert result_players[0].player_id == 101
        assert result_players[1].player_id == 102
        assert result_players[0].name == "Mock Player One"
        assert result_players[0].active is True
        assert result_players[1].active is False
        assert result_players[0].modified_at == datetime(2023, 10, 26, 10, 0, 0, tzinfo=timezone.utc)


@pytest.mark.asyncio
async def test_get_player_success(httpx_mock):
    """Test successfully getting a single player."""
    player_id_to_get = 101

    httpx_mock.add_response(
        url=f"{MOCK_BASE_URL}/auth/sign-in",
        method="POST",
        json=MOCK_LOGIN_SUCCESS_DATA,
        status_code=200
    )

    httpx_mock.add_response(
        url=f"{MOCK_BASE_URL}/players/{player_id_to_get}",
        method="GET",
        json=PLAYER_1,
        status_code=200
    )

    async with AsyncSession(base_url=MOCK_BASE_URL) as session:
        await session.login(email="mock@user.com", password="mockpassword")
        players_resource = Players(session)
        result_player = await players_resource.get_player(player_id_to_get)

        assert isinstance(result_player, Player)
        assert result_player.player_id == player_id_to_get
        assert result_player.name == "Mock Player One"


@pytest.mark.asyncio
async def test_get_player_not_found(httpx_mock):
    """Test handling of a 404 error when getting a player."""
    player_id_to_get = 999

    httpx_mock.add_response(
        url=f"{MOCK_BASE_URL}/auth/sign-in",
        method="POST",
        json=MOCK_LOGIN_SUCCESS_DATA,
        status_code=200
    )

    httpx_mock.add_response(
        url=f"{MOCK_BASE_URL}/players/{player_id_to_get}",
        method="GET",
        text="Player not found",
        status_code=404
    )

    async with AsyncSession(base_url=MOCK_BASE_URL) as session:
        await session.login(email="mock@user.com", password="mockpassword")
        players_resource = Players(session)

        with pytest.raises(EsourceCommunicationError) as excinfo:
            await players_resource.get_player(player_id_to_get)

        assert "HTTP Error: 404 Not Found" in str(excinfo.value)
        assert "Player not found" in str(excinfo.value)


@pytest.mark.asyncio
async def test_list_players_auth_error(httpx_mock):
    """Test handling of a 401 error when listing players."""

    httpx_mock.add_response(
        url=f"{MOCK_BASE_URL}/auth/sign-in",
        method="POST",
        json=MOCK_LOGIN_SUCCESS_DATA,
        status_code=200
    )

    httpx_mock.add_response(
        url=f"{MOCK_BASE_URL}/players",
        method="GET",
        text="Unauthorized",
        status_code=401
    )

    async with AsyncSession(base_url=MOCK_BASE_URL) as session:
        await session.login(email="mock@user.com", password="mockpassword")
        players_resource = Players(session)

        with pytest.raises(AuthenticationError) as excinfo:
            await players_resource.list_players()

        assert "Unauthorized access (401)" in str(excinfo.value)
        assert "Unauthorized" in str(excinfo.value)
