from client_api.session import Session
from client_api.sports import Sports
from conftest import API_URL, TEST_EMAIL, TEST_PASSWORD


def test_get_all_sports():
    session = Session(API_URL, TEST_EMAIL, TEST_PASSWORD)
    sports = Sports(session)

    response = sports.list_sports()

    assert isinstance(response, list)
    assert all("id" in sport and "name" in sport and "slug" for sport in response)


def test_get_sport_by_id():
    session = Session(API_URL, TEST_EMAIL, TEST_PASSWORD)
    sports = Sports(session)

    response = sports.get_sport(3)

    assert response["id"] == 3
    assert response["slug"] == "cs-go"
    assert response["name"] == "Counter-Strike"
