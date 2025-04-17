import httpx
import pytest

from esource_client_api.models.errors import EsourceCommunicationError, AuthenticationError
from esource_client_api.models.models import Team, TeamWithPlayers, Player
from esource_client_api.async_.teams import Teams
from esource_client_api.async_.session import AsyncSession
from conftest import MOCK_BASE_URL, MOCK_LOGIN_SUCCESS_DATA, TEAM_1
from tests.test_teams import MOCK_TEAM_WITH_PLAYERS_DATA, MOCK_TEAM_LIST_DATA

MOCK_TEAM_PLAYERS_RESPONSE_DATA = [MOCK_TEAM_WITH_PLAYERS_DATA]


@pytest.mark.asyncio
async def test_list_teams_success(httpx_mock):
    """Test successfully listing teams."""
    httpx_mock.add_response(
        url=f"{MOCK_BASE_URL}/auth/sign-in", method="POST", json=MOCK_LOGIN_SUCCESS_DATA, status_code=200
    )
    httpx_mock.add_response(
        url=f"{MOCK_BASE_URL}/teams", method="GET", json=MOCK_TEAM_LIST_DATA, status_code=200
    )

    async with AsyncSession(base_url=MOCK_BASE_URL) as session:
        await session.login(email="mock@user.com", password="mockpassword")
        teams_resource = Teams(session)
        result_teams = await teams_resource.list_teams()

        assert isinstance(result_teams, list)
        assert len(result_teams) == 2
        assert all(isinstance(t, Team) for t in result_teams)
        assert result_teams[0].team_id == 201
        assert result_teams[0].name == "Alpha Team"
        assert result_teams[1].team_id == 202
        assert result_teams[1].acronym == "BT"


@pytest.mark.asyncio
async def test_list_teams_with_params_success(httpx_mock):
    """Test listing teams with query parameters."""
    httpx_mock.add_response(
        url=f"{MOCK_BASE_URL}/auth/sign-in", method="POST", json=MOCK_LOGIN_SUCCESS_DATA, status_code=200
    )

    expected_params = {"skip": "5", "take": "2", "search": "Alpha", "orderBy": "name", "orderDir": "desc"}
    expected_url = httpx.URL(f"{MOCK_BASE_URL}/teams", params=expected_params)

    httpx_mock.add_response(
        url=str(expected_url),
        method="GET",
        json=[TEAM_1],
        status_code=200
    )

    async with AsyncSession(base_url=MOCK_BASE_URL) as session:
        await session.login(email="mock@user.com", password="mockpassword")
        teams_resource = Teams(session)
        result_teams = await teams_resource.list_teams(skip=5, take=2, search="Alpha", order_by={"name": "desc"})

        assert isinstance(result_teams, list)
        assert len(result_teams) >= 0
        if result_teams:
            assert isinstance(result_teams[0], Team)
            assert result_teams[0].name == "Alpha Team"


@pytest.mark.asyncio
async def test_get_team_success(httpx_mock):
    """Test successfully getting a single team."""
    team_id_to_get = 201
    httpx_mock.add_response(
        url=f"{MOCK_BASE_URL}/auth/sign-in", method="POST", json=MOCK_LOGIN_SUCCESS_DATA, status_code=200
    )
    httpx_mock.add_response(
        url=f"{MOCK_BASE_URL}/teams/{team_id_to_get}", method="GET", json=TEAM_1, status_code=200
    )

    async with AsyncSession(base_url=MOCK_BASE_URL) as session:
        await session.login(email="mock@user.com", password="mockpassword")
        teams_resource = Teams(session)
        result_team = await teams_resource.get_team(team_id_to_get)

        assert isinstance(result_team, Team)
        assert result_team.team_id == team_id_to_get
        assert result_team.name == "Alpha Team"
        assert result_team.location == "West"


@pytest.mark.asyncio
async def test_get_team_not_found(httpx_mock):
    """Test handling 404 when getting a team."""
    team_id_to_get = 999
    httpx_mock.add_response(
        url=f"{MOCK_BASE_URL}/auth/sign-in", method="POST", json=MOCK_LOGIN_SUCCESS_DATA, status_code=200
    )
    httpx_mock.add_response(
        url=f"{MOCK_BASE_URL}/teams/{team_id_to_get}", method="GET", text="Team Not Found", status_code=404
    )

    async with AsyncSession(base_url=MOCK_BASE_URL) as session:
        await session.login(email="mock@user.com", password="mockpassword")
        teams_resource = Teams(session)

        with pytest.raises(EsourceCommunicationError) as excinfo:
            await teams_resource.get_team(team_id_to_get)
        assert "HTTP Error: 404 Not Found" in str(excinfo.value)
        assert "Team Not Found" in str(excinfo.value)


@pytest.mark.asyncio
async def test_get_team_players_success(httpx_mock):
    """Test getting a team with its players."""
    team_id_to_get = 201
    httpx_mock.add_response(
        url=f"{MOCK_BASE_URL}/auth/sign-in", method="POST", json=MOCK_LOGIN_SUCCESS_DATA, status_code=200
    )

    httpx_mock.add_response(
        url=f"{MOCK_BASE_URL}/teams/{team_id_to_get}/players",
        method="GET",
        json=MOCK_TEAM_PLAYERS_RESPONSE_DATA,
        status_code=200
    )

    async with AsyncSession(base_url=MOCK_BASE_URL) as session:
        await session.login(email="mock@user.com", password="mockpassword")
        teams_resource = Teams(session)
        result_team_players_list = await teams_resource.get_team_players(team_id_to_get)

        assert isinstance(result_team_players_list, list)
        assert len(result_team_players_list) == 1
        result_team_with_players = result_team_players_list[0]

        assert isinstance(result_team_with_players, TeamWithPlayers)
        assert result_team_with_players.team_id == team_id_to_get
        assert result_team_with_players.name == "Alpha Team"

        assert isinstance(result_team_with_players.players, list)
        assert len(result_team_with_players.players) == 2
        assert all(isinstance(p, Player) for p in result_team_with_players.players)
        assert result_team_with_players.players[0].player_id == 101
        assert result_team_with_players.players[1].name == "Mock Player Two"


@pytest.mark.asyncio
async def test_get_team_players_team_not_found(httpx_mock):
    """Test handling 404 when getting team players."""
    team_id_to_get = 999
    httpx_mock.add_response(
        url=f"{MOCK_BASE_URL}/auth/sign-in", method="POST", json=MOCK_LOGIN_SUCCESS_DATA, status_code=200
    )
    httpx_mock.add_response(
        url=f"{MOCK_BASE_URL}/teams/{team_id_to_get}/players",
        method="GET",
        text="Team Not Found",
        status_code=404
    )

    async with AsyncSession(base_url=MOCK_BASE_URL) as session:
        await session.login(email="mock@user.com", password="mockpassword")
        teams_resource = Teams(session)

        with pytest.raises(EsourceCommunicationError) as excinfo:
            await teams_resource.get_team_players(team_id_to_get)
        assert "HTTP Error: 404 Not Found" in str(excinfo.value)
        assert "Team Not Found" in str(excinfo.value)


@pytest.mark.asyncio
async def test_list_teams_auth_error(httpx_mock):
    """Test handling 401 when listing teams."""
    httpx_mock.add_response(
        url=f"{MOCK_BASE_URL}/auth/sign-in", method="POST", json=MOCK_LOGIN_SUCCESS_DATA, status_code=200
    )
    httpx_mock.add_response(
        url=f"{MOCK_BASE_URL}/teams", method="GET", text="Unauthorized", status_code=401
    )

    async with AsyncSession(base_url=MOCK_BASE_URL) as session:
        await session.login(email="mock@user.com", password="mockpassword")
        teams_resource = Teams(session)

        with pytest.raises(AuthenticationError) as excinfo:
            await teams_resource.list_teams()

        assert "Unauthorized access (401)" in str(excinfo.value)
        assert "Unauthorized" in str(excinfo.value)
