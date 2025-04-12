import pytest
from datetime import datetime, timezone

from client_api.session import AuthenticationError, EsourceCommunicationError
from client_api.players import Players
from client_api.models import Player
from conftest import create_mock_response, PLAYER_1, PLAYER_2


MOCK_PLAYER_LIST_DATA = [PLAYER_1, PLAYER_2]


def test_list_players_success(mock_session, mocker):
    """Test successfully listing players with mock data."""
    session, mock_request = mock_session

    headers = {"Content-Type": "application/json", "Authorization": session.token}
    mock_api_resp = create_mock_response(mocker, 200, json_data=MOCK_PLAYER_LIST_DATA, headers=headers)
    mock_request.return_value = mock_api_resp

    players_resource = Players(session)
    result_players = players_resource.list_players(skip=10, take=5, search="Mock", order_by={"name": "desc"})

    assert isinstance(result_players, list)
    assert len(result_players) == 2
    assert result_players[0].playerId == 101
    assert result_players[1].playerId == 102
    assert result_players[0].name == "Mock Player One"
    assert result_players[0].active is True
    assert result_players[1].active is False
    assert result_players[0].modifiedAt == datetime(2023, 10, 26, 10, 0, 0, tzinfo=timezone.utc)


def test_get_player_success(mock_session, mocker):
    """Test successfully getting a single player."""
    session, mock_request = mock_session
    player_id_to_get = 101

    mock_api_resp = create_mock_response(mocker, 200, json_data=PLAYER_1)
    mock_request.return_value = mock_api_resp

    players_resource = Players(session)
    result_player = players_resource.get_player(player_id_to_get)

    assert isinstance(result_player, Player)
    assert result_player.playerId == player_id_to_get
    assert result_player.name == "Mock Player One"


def test_get_player_not_found(mock_session, mocker):
    """Test handling of a 404 error when getting a player."""
    session, mock_request = mock_session
    player_id_to_get = 999

    mock_api_resp = create_mock_response(mocker, 404, text_data="Player not found")
    mock_request.return_value = mock_api_resp

    players_resource = Players(session)

    with pytest.raises(EsourceCommunicationError) as excinfo:
        players_resource.get_player(player_id_to_get)

    assert "HTTP Error: 404 Not Found" in str(excinfo.value)


def test_list_players_auth_error(mock_session, mocker):
    """Test handling of a 401 error when listing players."""
    session, mock_request = mock_session

    mock_api_resp = create_mock_response(mocker, 401, text_data="Unauthorized")
    mock_request.return_value = mock_api_resp

    players_resource = Players(session)

    with pytest.raises(AuthenticationError) as excinfo:
        players_resource.list_players()

    assert "Unauthorized access (401)" in str(excinfo.value)
