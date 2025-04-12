import pytest
from datetime import datetime, timezone

from client_api.trading_events import TradingEvents
from client_api.models import TradingEvent, TradingMarket, TradingOutcome, Sport
from client_api.session import AuthenticationError, EsourceCommunicationError

from conftest import create_mock_response, TRADING_EVENT_1, TRADING_EVENT_2

MOCK_EVENT_LIST_DATA = [TRADING_EVENT_1, TRADING_EVENT_2]


def test_list_trading_events_success(mock_session, mocker):
    session, mock_request = mock_session

    mock_api_resp = create_mock_response(mocker, 200, json_data=MOCK_EVENT_LIST_DATA)
    mock_request.return_value = mock_api_resp

    trading_events = TradingEvents(session)
    result_events = trading_events.list_trading_events()

    assert isinstance(result_events, list)
    assert len(result_events) == 2
    assert all(isinstance(e, TradingEvent) for e in result_events)

    assert result_events[0].id == 401
    assert result_events[0].name == "Team A vs Team B - Grand Final"
    assert result_events[1].id == 402
    assert result_events[1].status == "Suspended"

    assert isinstance(result_events[0].sport, Sport)
    assert result_events[0].sport.slug == "cs-go"

    assert isinstance(result_events[0].tradingMarkets, list)
    assert len(result_events[0].tradingMarkets) == 1
    assert isinstance(result_events[0].tradingMarkets[0], TradingMarket)
    assert result_events[0].tradingMarkets[0].marketKey == "H2H"
    assert isinstance(result_events[0].tradingMarkets[0].outcomes, list)
    assert len(result_events[0].tradingMarkets[0].outcomes) == 2
    assert isinstance(result_events[0].tradingMarkets[0].outcomes[0], TradingOutcome)
    assert result_events[0].tradingMarkets[0].outcomes[0].price == 1.85

    assert isinstance(result_events[1].tradingMarkets, list)
    assert len(result_events[1].tradingMarkets) == 0


def test_list_trading_events_with_filters_success(mock_session, mocker):
    session, mock_request = mock_session

    mock_api_resp = create_mock_response(mocker, 200, json_data=[TRADING_EVENT_1])
    mock_request.return_value = mock_api_resp

    events_resource = TradingEvents(session)
    result_events = events_resource.list_trading_events(
        sport_id=1,
        trading_tournament_id=123,
        statuses="Open,Suspended",
        search="Final",
        skip=0,
        take=10
    )

    assert isinstance(result_events, list)
    assert len(result_events) >= 0
    if result_events:
        assert isinstance(result_events[0], TradingEvent)


def test_get_trading_event_success(mock_session, mocker):
    session, mock_request = mock_session
    event_id_to_get = 401

    mock_api_resp = create_mock_response(mocker, 200, json_data=TRADING_EVENT_1)
    mock_request.return_value = mock_api_resp

    events_resource = TradingEvents(session)
    result_event = events_resource.get_trading_event(event_id_to_get)

    assert isinstance(result_event, TradingEvent)
    assert result_event.id == event_id_to_get
    assert result_event.name == "Team A vs Team B - Grand Final"
    assert result_event.status == "Open"
    assert result_event.beginAt == datetime(2025, 5, 1, 18, 0, 0, tzinfo=timezone.utc)
    assert isinstance(result_event.sport, Sport)
    assert result_event.sport.id == 3
    assert isinstance(result_event.tradingMarkets, list)
    assert len(result_event.tradingMarkets) == 1
    assert isinstance(result_event.tradingMarkets[0], TradingMarket)
    assert len(result_event.tradingMarkets[0].outcomes) == 2
    assert isinstance(result_event.tradingMarkets[0].outcomes[0], TradingOutcome)


def test_get_trading_event_not_found(mock_session, mocker):
    session, mock_request = mock_session
    event_id_to_get = 999

    mock_api_resp = create_mock_response(mocker, 404, text_data="Event Not Found")
    mock_request.return_value = mock_api_resp

    events_resource = TradingEvents(session)

    with pytest.raises(EsourceCommunicationError) as excinfo:
        events_resource.get_trading_event(event_id_to_get)
    assert "HTTP Error: 404 Not Found" in str(excinfo.value)


def test_list_trading_events_auth_error(mock_session, mocker):
    session, mock_request = mock_session

    mock_api_resp = create_mock_response(mocker, 401, text_data="Unauthorized")
    mock_request.return_value = mock_api_resp

    events_resource = TradingEvents(session)

    with pytest.raises(AuthenticationError):
        events_resource.list_trading_events()
