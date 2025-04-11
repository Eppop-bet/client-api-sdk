import pytest
import requests.exceptions

from client_api.teams import Teams
from client_api.models import Team, TeamWithPlayers, Player
from client_api.session import AuthenticationError, EsourceCommunicationError

from conftest import create_mock_response


MOCK_PLAYER_TEAM_DATA_1 = {
    "playerId": 501, "name": "Team Player A", "firstName": "Team", "lastName": "Player A",
    "active": True, "age": 22, "birthday": "2001-03-10T00:00:00Z", "imageUrl": None,
    "modifiedAt": "2023-11-01T10:00:00Z", "nationality": "Testland", "role": "Entry", "slug": "team-player-a"
}
MOCK_PLAYER_TEAM_DATA_2 = {
    "playerId": 502, "name": "Team Player B", "firstName": "Team", "lastName": "Player B",
    "active": True, "age": 24, "birthday": "1999-07-20T00:00:00Z", "imageUrl": None,
    "modifiedAt": "2023-11-02T11:00:00Z", "nationality": "Testland", "role": "Support", "slug": "team-player-b"
}

MOCK_TEAM_1_DATA = {
    "teamId": 201, "name": "Alpha Team", "slug": "alpha-team", "acronym": "AT",
    "imageUrl": "http://example.com/alpha.png", "location": "West", "modifiedAt": "2023-10-10T12:00:00Z"
}
MOCK_TEAM_2_DATA = {
    "teamId": 202, "name": "Bravo Team", "slug": "bravo-team", "acronym": "BT",
    "imageUrl": None, "location": "East", "modifiedAt": "2023-10-11T13:00:00Z"
}
MOCK_TEAM_LIST_DATA = [MOCK_TEAM_1_DATA, MOCK_TEAM_2_DATA]

MOCK_TEAM_WITH_PLAYERS_DATA = {
    **MOCK_TEAM_1_DATA,
    "players": [MOCK_PLAYER_TEAM_DATA_1, MOCK_PLAYER_TEAM_DATA_2]
}
MOCK_TEAM_PLAYERS_RESPONSE_DATA = [MOCK_TEAM_WITH_PLAYERS_DATA]



def test_list_teams_success(mock_session, mocker):
    session, mock_request = mock_session

    mock_api_resp = create_mock_response(mocker, 200, json_data=MOCK_TEAM_LIST_DATA)
    mock_request.return_value = mock_api_resp

    teams_resource = Teams(session)
    result_teams = teams_resource.list_teams()

    assert isinstance(result_teams, list)
    assert len(result_teams) == 2
    assert all(isinstance(t, Team) for t in result_teams)
    assert result_teams[0].teamId == 201
    assert result_teams[0].name == "Alpha Team"
    assert result_teams[1].teamId == 202
    assert result_teams[1].acronym == "BT"


def test_list_teams_with_params_success(mock_session, mocker):
    session, mock_request = mock_session

    mock_api_resp = create_mock_response(mocker, 200, json_data=[MOCK_TEAM_1_DATA])
    mock_request.return_value = mock_api_resp

    teams_resource = Teams(session)
    result_teams = teams_resource.list_teams(skip=5, take=2, search="Alpha", order_by={"name": "desc"})

    assert isinstance(result_teams, list)
    assert len(result_teams) >= 0
    if result_teams:
        assert isinstance(result_teams[0], Team)


def test_get_team_success(mock_session, mocker):
    session, mock_request = mock_session
    team_id_to_get = 201

    mock_api_resp = create_mock_response(mocker, 200, json_data=MOCK_TEAM_1_DATA)
    mock_request.return_value = mock_api_resp

    teams_resource = Teams(session)
    result_team = teams_resource.get_team(team_id_to_get)

    assert isinstance(result_team, Team)
    assert result_team.teamId == team_id_to_get
    assert result_team.name == "Alpha Team"
    assert result_team.location == "West"


def test_get_team_not_found(mock_session, mocker):
    session, mock_request = mock_session
    team_id_to_get = 999

    mock_api_resp = create_mock_response(mocker, 404, text_data="Team Not Found")
    mock_request.return_value = mock_api_resp

    teams_resource = Teams(session)

    with pytest.raises(EsourceCommunicationError) as excinfo:
        teams_resource.get_team(team_id_to_get)
    assert "HTTP Error: 404 Not Found" in str(excinfo.value)


def test_get_team_players_success(mock_session, mocker):
    session, mock_request = mock_session
    team_id_to_get = 201

    mock_api_resp = create_mock_response(mocker, 200, json_data=MOCK_TEAM_PLAYERS_RESPONSE_DATA)
    mock_request.return_value = mock_api_resp

    teams_resource = Teams(session)
    result_team_players_list = teams_resource.get_team_players(team_id_to_get)

    assert isinstance(result_team_players_list, list)
    assert len(result_team_players_list) == 1
    result_team_with_players = result_team_players_list[0]

    assert isinstance(result_team_with_players, TeamWithPlayers)
    assert result_team_with_players.teamId == team_id_to_get
    assert result_team_with_players.name == "Alpha Team"

    assert isinstance(result_team_with_players.players, list)
    assert len(result_team_with_players.players) == 2
    assert all(isinstance(p, Player) for p in result_team_with_players.players)
    assert result_team_with_players.players[0].playerId == 501
    assert result_team_with_players.players[1].name == "Team Player B"


def test_get_team_players_team_not_found(mock_session, mocker):
    session, mock_request = mock_session
    team_id_to_get = 999

    mock_api_resp = create_mock_response(mocker, 404, text_data="Team Not Found")
    mock_request.return_value = mock_api_resp

    teams_resource = Teams(session)

    with pytest.raises(EsourceCommunicationError) as excinfo:
        teams_resource.get_team_players(team_id_to_get)
    assert "HTTP Error: 404 Not Found" in str(excinfo.value)


def test_list_teams_auth_error(mock_session, mocker):
    session, mock_request = mock_session

    mock_api_resp = create_mock_response(mocker, 401, text_data="Unauthorized")
    mock_request.return_value = mock_api_resp

    teams_resource = Teams(session)

    with pytest.raises(AuthenticationError):
        teams_resource.list_teams()
