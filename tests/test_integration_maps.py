from client_api.session import Session
from client_api.maps import Maps
from conftest import API_URL, TEST_EMAIL, TEST_PASSWORD


def test_get_all_maps():
    session = Session(API_URL, TEST_EMAIL, TEST_PASSWORD)
    maps = Maps(session)

    response = maps.list_maps()

    assert isinstance(response, list)
    assert all("mapId" in m and "name" in m and "slug" for m in response)


def test_get_map_by_id():
    session = Session(API_URL, TEST_EMAIL, TEST_PASSWORD)
    maps = Maps(session)

    response = maps.get_map(3)

    assert response["mapId"] == 3
    assert response["slug"] == "train"
    assert response["name"] == "Train"


def test_get_map_by_name():
    session = Session(API_URL, TEST_EMAIL, TEST_PASSWORD)
    maps = Maps(session)
    response = maps.list_maps(search="Train")

    assert isinstance(response, list)
    assert response[0]["mapId"] == 3
    assert response[0]["slug"] == "train"
    assert response[0]["name"] == "Train"
