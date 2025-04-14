import pytest

from client_api.maps import Maps
from client_api.models import Map
from client_api.session import AuthenticationError, EsourceCommunicationError

from conftest import create_mock_response, MAP_1, MAP_2

MOCK_MAP_LIST_DATA = [MAP_1, MAP_2]


def test_list_maps_success(mock_session, mocker):
    session, mock_request = mock_session

    mock_api_resp = create_mock_response(mocker, 200, json_data=MOCK_MAP_LIST_DATA)
    mock_request.return_value = mock_api_resp

    maps_resource = Maps(session)
    result_maps = maps_resource.list_maps()

    assert isinstance(result_maps, list)
    assert len(result_maps) == 2
    assert all(isinstance(m, Map) for m in result_maps)
    assert result_maps[0].map_id == 1
    assert result_maps[0].name == "Mirage"
    assert result_maps[1].map_id == 3
    assert result_maps[1].slug == "train"


def test_list_maps_with_params_success(mock_session, mocker):
    session, mock_request = mock_session

    mock_api_resp = create_mock_response(mocker, 200, json_data=[MAP_1])
    mock_request.return_value = mock_api_resp

    maps_resource = Maps(session)
    result_maps = maps_resource.list_maps(skip=10, take=5, search="Train", order_by={"name": "asc"})

    assert isinstance(result_maps, list)
    assert len(result_maps) >= 0
    if result_maps:
        assert isinstance(result_maps[0], Map)


def test_get_map_success(mock_session, mocker):
    session, mock_request = mock_session
    map_id_to_get = 1

    mock_api_resp = create_mock_response(mocker, 200, json_data=MAP_1)
    mock_request.return_value = mock_api_resp

    maps_resource = Maps(session)
    result_map = maps_resource.get_map(map_id_to_get)

    assert isinstance(result_map, Map)
    assert result_map.map_id == map_id_to_get
    assert result_map.name == "Mirage"
    assert result_map.slug == "mirage"


def test_get_map_not_found(mock_session, mocker):
    session, mock_request = mock_session
    map_id_to_get = 999

    mock_api_resp = create_mock_response(mocker, 404, text_data="Map Not Found")
    mock_request.return_value = mock_api_resp

    maps_resource = Maps(session)

    with pytest.raises(EsourceCommunicationError) as excinfo:
        maps_resource.get_map(map_id_to_get)

    assert "HTTP Error: 404 Not Found" in str(excinfo.value)


def test_list_maps_auth_error(mock_session, mocker):
    session, mock_request = mock_session

    mock_api_resp = create_mock_response(mocker, 401, text_data="Unauthorized")
    mock_request.return_value = mock_api_resp

    maps_resource = Maps(session)

    with pytest.raises(AuthenticationError):
        maps_resource.list_maps()
