import pytest

from client_api.session import AuthenticationError, EsourceCommunicationError
from client_api.sports import Sports
from client_api.models import Sport
from conftest import create_mock_response, SPORT_1, SPORT_2


MOCK_SPORT_LIST_DATA = [SPORT_1, SPORT_2]

def test_list_sports_success(mock_session, mocker):
    """Test successfully listing sports with mock data."""
    session, mock_request = mock_session

    headers = {"Content-Type": "application/json", "Authorization": session.token}
    mock_api_resp = create_mock_response(mocker, 200, json_data=MOCK_SPORT_LIST_DATA, headers=headers)
    mock_request.return_value = mock_api_resp

    sports_resource = Sports(session)
    result_sports = sports_resource.list_sports()

    assert isinstance(result_sports, list)
    assert len(result_sports) == 2
    assert isinstance(result_sports[0], Sport)
    assert result_sports[0].id == 3
    assert result_sports[1].slug == "lol"


def test_get_sport_success(mock_session, mocker):
    """Test successfully getting a single sport."""
    session, mock_request = mock_session
    sport_id_to_get = 3

    mock_api_resp = create_mock_response(mocker, 200, json_data=SPORT_1)
    mock_request.return_value = mock_api_resp

    sports_resource = Sports(session)
    result_sport = sports_resource.get_sport(sport_id_to_get)

    assert isinstance(result_sport, Sport)
    assert result_sport.id == sport_id_to_get
    assert result_sport.name == "Counter-Strike"


def test_get_sport_not_found(mock_session, mocker):
    """Test handling of a 404 error when getting a sport."""
    session, mock_request = mock_session
    sport_id_to_get = 999

    mock_api_resp = create_mock_response(mocker, 404, text_data="Not Found")
    mock_request.return_value = mock_api_resp

    sports_resource = Sports(session)

    with pytest.raises(EsourceCommunicationError) as excinfo:
        sports_resource.get_sport(sport_id_to_get)

    assert "HTTP Error: 404 Not Found" in str(excinfo.value)


def test_list_sports_auth_error(mock_session, mocker):
    """Test handling of a 401 error when listing sports."""
    session, mock_request = mock_session

    mock_api_resp = create_mock_response(mocker, 401, text_data="Unauthorized")
    mock_request.return_value = mock_api_resp

    sports_resource = Sports(session)

    with pytest.raises(AuthenticationError) as excinfo:
        sports_resource.list_sports()
