import httpx
import pytest

from esource_client_api.async_.trading_tournaments import TradingTournaments
from esource_client_api.async_.session import AsyncSession
from conftest import TOURNAMENT_1, TOURNAMENT_2, TOURNAMENT_3, MOCK_BASE_URL_V1, MOCK_LOGIN_SUCCESS_DATA, MOCK_BASE_URL
from esource_client_api.models.errors import EsourceCommunicationError, AuthenticationError
from esource_client_api.models.models import TradingTournament

MOCK_TOURNAMENT_LIST_DATA = [TOURNAMENT_1, TOURNAMENT_2, TOURNAMENT_3]


@pytest.mark.asyncio
async def test_list_trading_tournaments_success(httpx_mock):
    """Test successfully listing trading tournaments."""
    httpx_mock.add_response(
        url=f"{MOCK_BASE_URL_V1}/auth/sign-in", method="POST", json=MOCK_LOGIN_SUCCESS_DATA, status_code=200
    )
    httpx_mock.add_response(
        url=f"{MOCK_BASE_URL_V1}/trading-tournaments", method="GET", json=MOCK_TOURNAMENT_LIST_DATA, status_code=200
    )

    async with AsyncSession(base_url=MOCK_BASE_URL) as session:
        await session.login(email="mock@user.com", password="mockpassword")

        tournaments_resource = TradingTournaments(session)
        result_tournaments = await tournaments_resource.list_trading_tournaments()

        assert isinstance(result_tournaments, list)
        assert len(result_tournaments) == 3
        assert all(isinstance(t, TradingTournament) for t in result_tournaments)
        assert result_tournaments[0].id == 301
        assert result_tournaments[0].name == "Major Championship"
        assert result_tournaments[1].id == 302
        assert result_tournaments[1].trading_category_id is None


@pytest.mark.asyncio
async def test_list_trading_tournaments_with_filters_success(httpx_mock):
    """Test listing trading tournaments with filters."""
    httpx_mock.add_response(
        url=f"{MOCK_BASE_URL_V1}/auth/sign-in", method="POST", json=MOCK_LOGIN_SUCCESS_DATA, status_code=200
    )

    expected_params = {
        "sportId": "1",
        "tradingCategoryId": "10",
        "search": "Major",
        "skip": "0",
        "take": "10"
    }
    expected_url = httpx.URL(f"{MOCK_BASE_URL_V1}/trading-tournaments", params=expected_params)

    mock_filtered_data = [TOURNAMENT_1]
    httpx_mock.add_response(
        url=str(expected_url),
        method="GET",
        json=mock_filtered_data,
        status_code=200
    )

    async with AsyncSession(base_url=MOCK_BASE_URL) as session:
        await session.login(email="mock@user.com", password="mockpassword")
        tournaments_resource = TradingTournaments(session)
        result_tournaments = await tournaments_resource.list_trading_tournaments(
            sport_id=1,
            trading_category_id=10,
            search="Major",
            skip=0,
            take=10
        )

        assert isinstance(result_tournaments, list)
        assert len(result_tournaments) == len(mock_filtered_data)
        if result_tournaments:
            assert isinstance(result_tournaments[0], TradingTournament)
            assert result_tournaments[0].id == TOURNAMENT_1["id"]


@pytest.mark.asyncio
async def test_get_trading_tournament_success(httpx_mock):
    """Test successfully getting a single trading tournament."""
    tournament_id_to_get = 301
    httpx_mock.add_response(
        url=f"{MOCK_BASE_URL_V1}/auth/sign-in", method="POST", json=MOCK_LOGIN_SUCCESS_DATA, status_code=200
    )
    httpx_mock.add_response(
        url=f"{MOCK_BASE_URL_V1}/trading-tournaments/{tournament_id_to_get}",
        method="GET",
        json=TOURNAMENT_1,
        status_code=200
    )

    async with AsyncSession(base_url=MOCK_BASE_URL) as session:
        await session.login(email="mock@user.com", password="mockpassword")
        tournaments_resource = TradingTournaments(session)
        result_tournament = await tournaments_resource.get_trading_tournament(tournament_id_to_get)

        assert isinstance(result_tournament, TradingTournament)
        assert result_tournament.id == tournament_id_to_get
        assert result_tournament.name == "Major Championship"
        assert result_tournament.sport_id == 1
        assert result_tournament.trading_category_id == 10


@pytest.mark.asyncio
async def test_get_trading_tournament_not_found(httpx_mock):
    """Test handling 404 when getting a trading tournament."""
    tournament_id_to_get = 999
    httpx_mock.add_response(
        url=f"{MOCK_BASE_URL_V1}/auth/sign-in", method="POST", json=MOCK_LOGIN_SUCCESS_DATA, status_code=200
    )
    httpx_mock.add_response(
        url=f"{MOCK_BASE_URL_V1}/trading-tournaments/{tournament_id_to_get}",
        method="GET",
        text="Tournament Not Found",
        status_code=404
    )

    async with AsyncSession(base_url=MOCK_BASE_URL) as session:
        await session.login(email="mock@user.com", password="mockpassword")
        tournaments_resource = TradingTournaments(session)

        with pytest.raises(EsourceCommunicationError) as excinfo:
            await tournaments_resource.get_trading_tournament(tournament_id_to_get)
        assert "HTTP Error: 404 Not Found" in str(excinfo.value)
        assert "Tournament Not Found" in str(excinfo.value)


@pytest.mark.asyncio
async def test_list_trading_tournaments_auth_error(httpx_mock):
    """Test handling 401 when listing trading tournaments."""
    httpx_mock.add_response(
        url=f"{MOCK_BASE_URL_V1}/auth/sign-in", method="POST", json=MOCK_LOGIN_SUCCESS_DATA, status_code=200
    )
    httpx_mock.add_response(
        url=f"{MOCK_BASE_URL_V1}/trading-tournaments", method="GET", text="Unauthorized", status_code=401
    )

    async with AsyncSession(base_url=MOCK_BASE_URL) as session:
        await session.login(email="mock@user.com", password="mockpassword")
        tournaments_resource = TradingTournaments(session)

        with pytest.raises(AuthenticationError) as excinfo:
            await tournaments_resource.list_trading_tournaments()

        assert "Unauthorized access (401)" in str(excinfo.value)
        assert "Unauthorized" in str(excinfo.value)
