from client_api.session import Session
from client_api.players import Players
from client_api.models import Player
from conftest import API_URL, TEST_EMAIL, TEST_PASSWORD


def test_get_all_players():
    session = Session(API_URL, TEST_EMAIL, TEST_PASSWORD)
    players = Players(session)

    response = players.list_players()

    assert isinstance(response, list)
    assert all(isinstance(player, Player) for player in response)


def test_get_player_by_id():
    session = Session(API_URL, TEST_EMAIL, TEST_PASSWORD)
    player = Players(session)

    response = player.get_player(17497)

    assert response.playerId == 17497
    assert response.firstName == "Gabriel"
