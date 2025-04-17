import pytest

from esource_client_api.models.models import Sport
from esource_client_api.sync.session import Session
from esource_client_api.sync.sports import Sports
from conftest import API_URL, TEST_EMAIL, TEST_PASSWORD


@pytest.mark.integration
def test_get_all_sports():
    session = Session(API_URL, TEST_EMAIL, TEST_PASSWORD)
    sports = Sports(session)

    response = sports.list_sports()

    assert isinstance(response, list)
    assert all(isinstance(sport, Sport) for sport in response)


@pytest.mark.integration
def test_get_sport_by_id():
    session = Session(API_URL, TEST_EMAIL, TEST_PASSWORD)
    sports = Sports(session)

    response = sports.get_sport(3)

    assert response.id == 3
    assert response.slug == "cs-go"
    assert response.name == "Counter-Strike"
