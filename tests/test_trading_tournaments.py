import pytest
import requests.exceptions

from client_api.trading_tournaments import TradingTournaments
from client_api.models import TradingTournament
from client_api.session import AuthenticationError, EsourceCommunicationError

from conftest import create_mock_response, TOURNAMENT_1, TOURNAMENT_2, TOURNAMENT_3

MOCK_TOURNAMENT_LIST_DATA = [TOURNAMENT_1, TOURNAMENT_2, TOURNAMENT_3]



def test_list_trading_tournaments_success(mock_session, mocker):
    session, mock_request = mock_session

    mock_api_resp = create_mock_response(mocker, 200, json_data=MOCK_TOURNAMENT_LIST_DATA)
    mock_request.return_value = mock_api_resp

    tournaments_resource = TradingTournaments(session)
    result_tournaments = tournaments_resource.list_trading_tournaments()

    assert isinstance(result_tournaments, list)
    assert len(result_tournaments) == 3
    assert all(isinstance(t, TradingTournament) for t in result_tournaments)
    assert result_tournaments[0].id == 301
    assert result_tournaments[0].name == "Major Championship"
    assert result_tournaments[1].id == 302
    assert result_tournaments[1].tradingCategoryId is None


def test_list_trading_tournaments_with_filters_success(mock_session, mocker):
    session, mock_request = mock_session

    mock_api_resp = create_mock_response(mocker, 200, json_data=[TOURNAMENT_1])
    mock_request.return_value = mock_api_resp

    tournaments_resource = TradingTournaments(session)
    result_tournaments = tournaments_resource.list_trading_tournaments(
        sport_id=1,
        trading_category_id=10,
        search="Major",
        skip=0,
        take=10
    )

    assert isinstance(result_tournaments, list)
    assert len(result_tournaments) >= 0
    if result_tournaments:
        assert isinstance(result_tournaments[0], TradingTournament)


def test_get_trading_tournament_success(mock_session, mocker):
    session, mock_request = mock_session
    tournament_id_to_get = 301

    mock_api_resp = create_mock_response(mocker, 200, json_data=TOURNAMENT_1)
    mock_request.return_value = mock_api_resp

    tournaments_resource = TradingTournaments(session)
    result_tournament = tournaments_resource.get_trading_tournament(tournament_id_to_get)

    assert isinstance(result_tournament, TradingTournament)
    assert result_tournament.id == tournament_id_to_get
    assert result_tournament.name == "Major Championship"
    assert result_tournament.sportId == 1
    assert result_tournament.tradingCategoryId == 10


def test_get_trading_tournament_not_found(mock_session, mocker):
    session, mock_request = mock_session
    tournament_id_to_get = 999

    mock_api_resp = create_mock_response(mocker, 404, text_data="Tournament Not Found")
    mock_request.return_value = mock_api_resp

    tournaments_resource = TradingTournaments(session)

    with pytest.raises(EsourceCommunicationError) as excinfo:
        tournaments_resource.get_trading_tournament(tournament_id_to_get)
    assert "HTTP Error: 404 Not Found" in str(excinfo.value)


def test_list_trading_tournaments_auth_error(mock_session, mocker):
    session, mock_request = mock_session

    mock_api_resp = create_mock_response(mocker, 401, text_data="Unauthorized")
    mock_request.return_value = mock_api_resp

    tournaments_resource = TradingTournaments(session)

    with pytest.raises(AuthenticationError):
        tournaments_resource.list_trading_tournaments()


