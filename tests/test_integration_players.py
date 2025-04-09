from client_api.session import Session
from client_api.players import Players
from conftest import API_URL, TEST_EMAIL, TEST_PASSWORD


def test_get_all_players():
    session = Session(API_URL, TEST_EMAIL, TEST_PASSWORD)
    players = Players(session)

    response = players.list_players()

    assert isinstance(response, list)
    assert all("playerId" in player and "name" in player and "slug" for player in response)


def test_get_player_by_id():
    session = Session(API_URL, TEST_EMAIL, TEST_PASSWORD)
    player = Players(session)

    response = player.get_player(3)

    assert response["playerId"] == 3
