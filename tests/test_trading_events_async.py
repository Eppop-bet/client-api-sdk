import httpx
import pytest
from datetime import datetime, timezone

from esource_client_api.async_.trading_events import TradingEvents
from esource_client_api.models.errors import EsourceCommunicationError, AuthenticationError
from esource_client_api.models.models import TradingEvent, Sport, TradingMarket, TradingOutcome
from esource_client_api.async_.session import AsyncSession
from conftest import TRADING_EVENT_1, TRADING_EVENT_2, MOCK_BASE_URL_V1, MOCK_LOGIN_SUCCESS_DATA, MOCK_BASE_URL

MOCK_EVENT_LIST_DATA = [TRADING_EVENT_1, TRADING_EVENT_2]


@pytest.mark.asyncio
async def test_list_trading_events_success(httpx_mock):
    """Test successfully listing trading events."""
    httpx_mock.add_response(
        url=f"{MOCK_BASE_URL_V1}/auth/sign-in", method="POST", json=MOCK_LOGIN_SUCCESS_DATA, status_code=200
    )
    httpx_mock.add_response(
        url=f"{MOCK_BASE_URL_V1}/trading-events", method="GET", json=MOCK_EVENT_LIST_DATA, status_code=200
    )

    async with AsyncSession(base_url=MOCK_BASE_URL) as session:
        await session.login(email="mock@user.com", password="mockpassword")

        trading_events = TradingEvents(session)
        result_events = await trading_events.list_trading_events()

        assert isinstance(result_events, list)
        assert len(result_events) == 2
        assert all(isinstance(e, TradingEvent) for e in result_events)

        assert result_events[0].id == 401
        assert result_events[0].name == "Team A vs Team B - Grand Final"
        assert result_events[1].id == 402
        assert result_events[1].status == "Suspended"

        assert isinstance(result_events[0].sport, Sport)
        assert result_events[0].sport.slug == "cs-go"

        assert isinstance(result_events[0].trading_markets, list)
        assert len(result_events[0].trading_markets) == 1
        assert isinstance(result_events[0].trading_markets[0], TradingMarket)
        assert result_events[0].trading_markets[0].market_key == "H2H"
        assert isinstance(result_events[0].trading_markets[0].outcomes, list)
        assert len(result_events[0].trading_markets[0].outcomes) == 2
        assert isinstance(result_events[0].trading_markets[0].outcomes[0], TradingOutcome)
        assert result_events[0].trading_markets[0].outcomes[0].price == 1.85

        assert isinstance(result_events[1].trading_markets, list)
        assert len(result_events[1].trading_markets) == 0


@pytest.mark.asyncio
async def test_list_trading_events_with_filters_success(httpx_mock):
    """Test listing trading events with filters."""
    httpx_mock.add_response(
        url=f"{MOCK_BASE_URL_V1}/auth/sign-in", method="POST", json=MOCK_LOGIN_SUCCESS_DATA, status_code=200
    )

    expected_params = {
        "sportId": "1",
        "tradingTournamentId": "123",
        "statuses": "Open,Suspended",
        "search": "Final",
        "skip": "0",
        "take": "10"
    }
    expected_url = httpx.URL(f"{MOCK_BASE_URL_V1}/trading-events", params=expected_params)

    mock_filtered_data = [TRADING_EVENT_1]
    httpx_mock.add_response(
        url=str(expected_url),
        method="GET",
        json=mock_filtered_data,
        status_code=200
    )

    async with AsyncSession(base_url=MOCK_BASE_URL) as session:
        await session.login(email="mock@user.com", password="mockpassword")
        events_resource = TradingEvents(session)
        result_events = await events_resource.list_trading_events(
            sport_id=1,
            trading_tournament_id=123,
            statuses="Open,Suspended",
            search="Final",
            skip=0,
            take=10
        )

        assert isinstance(result_events, list)
        assert len(result_events) == len(mock_filtered_data)
        if result_events:
            assert isinstance(result_events[0], TradingEvent)
            assert result_events[0].id == TRADING_EVENT_1["id"]


@pytest.mark.asyncio
async def test_get_trading_event_success(httpx_mock):
    """Test successfully getting a single trading event."""
    event_id_to_get = 401
    httpx_mock.add_response(
        url=f"{MOCK_BASE_URL_V1}/auth/sign-in", method="POST", json=MOCK_LOGIN_SUCCESS_DATA, status_code=200
    )
    httpx_mock.add_response(
        url=f"{MOCK_BASE_URL_V1}/trading-events/{event_id_to_get}",
        method="GET",
        json=TRADING_EVENT_1,
        status_code=200
    )

    async with AsyncSession(base_url=MOCK_BASE_URL) as session:
        await session.login(email="mock@user.com", password="mockpassword")
        events_resource = TradingEvents(session)
        result_event = await events_resource.get_trading_event(event_id_to_get)

        assert isinstance(result_event, TradingEvent)
        assert result_event.id == event_id_to_get
        assert result_event.name == "Team A vs Team B - Grand Final"
        assert result_event.status == "Open"
        assert result_event.begin_at == datetime(2025, 5, 1, 18, 0, 0, tzinfo=timezone.utc)
        assert isinstance(result_event.sport, Sport)
        assert result_event.sport.id == 3
        assert isinstance(result_event.trading_markets, list)
        assert len(result_event.trading_markets) == 1
        assert isinstance(result_event.trading_markets[0], TradingMarket)
        assert len(result_event.trading_markets[0].outcomes) == 2
        assert isinstance(result_event.trading_markets[0].outcomes[0], TradingOutcome)


@pytest.mark.asyncio
async def test_get_trading_event_not_found(httpx_mock):
    """Test handling 404 when getting a trading event."""
    event_id_to_get = 999
    httpx_mock.add_response(
        url=f"{MOCK_BASE_URL_V1}/auth/sign-in", method="POST", json=MOCK_LOGIN_SUCCESS_DATA, status_code=200
    )
    httpx_mock.add_response(
        url=f"{MOCK_BASE_URL_V1}/trading-events/{event_id_to_get}",
        method="GET",
        text="Event Not Found",
        status_code=404
    )

    async with AsyncSession(base_url=MOCK_BASE_URL) as session:
        await session.login(email="mock@user.com", password="mockpassword")
        events_resource = TradingEvents(session)

        with pytest.raises(EsourceCommunicationError) as excinfo:
            await events_resource.get_trading_event(event_id_to_get)
        assert "HTTP Error: 404 Not Found" in str(excinfo.value)
        assert "Event Not Found" in str(excinfo.value)


@pytest.mark.asyncio
async def test_list_trading_events_auth_error(httpx_mock):
    """Test handling 401 when listing trading events."""
    httpx_mock.add_response(
        url=f"{MOCK_BASE_URL_V1}/auth/sign-in", method="POST", json=MOCK_LOGIN_SUCCESS_DATA, status_code=200
    )
    httpx_mock.add_response(
        url=f"{MOCK_BASE_URL_V1}/trading-events", method="GET", text="Unauthorized", status_code=401
    )

    async with AsyncSession(base_url=MOCK_BASE_URL) as session:
        await session.login(email="mock@user.com", password="mockpassword")
        events_resource = TradingEvents(session)

        with pytest.raises(AuthenticationError) as excinfo:
            await events_resource.list_trading_events()

        assert "Unauthorized access (401)" in str(excinfo.value)
        assert "Unauthorized" in str(excinfo.value)
