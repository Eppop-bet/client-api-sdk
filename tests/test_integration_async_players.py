import pytest

from conftest import API_URL, TEST_EMAIL, TEST_PASSWORD
from esource_client_api.async_.players import Players
from esource_client_api.async_.session import AsyncSession
from esource_client_api.models.errors import AuthenticationError, EsourceCommunicationError
from esource_client_api.models.models import Player


@pytest.mark.asyncio
@pytest.mark.integration
async def test_get_all_players():
    session = AsyncSession(API_URL, TEST_EMAIL, TEST_PASSWORD)
    await session.login()

    players = Players(session)

    response = await players.list_players()

    assert isinstance(response, list)
    assert all(isinstance(player, Player) for player in response)


@pytest.mark.asyncio
@pytest.mark.integration
async def test_get_player_by_id():
    session = AsyncSession(API_URL, TEST_EMAIL, TEST_PASSWORD)
    await session.login()

    player = Players(session)

    response = await player.get_player(17497)

    assert response.player_id == 17497
    assert response.first_name == "Gabriel"


@pytest.mark.asyncio
@pytest.mark.integration
async def test_players_list_take():
    """Tests the 'take' query parameter limits results."""
    num_to_take = 2
    try:
        session = AsyncSession(API_URL, TEST_EMAIL, TEST_PASSWORD)
        await session.login()

        players_resource = Players(session)
        response = await players_resource.list_players(take=num_to_take)

        assert isinstance(response, list)
        assert len(response) <= num_to_take
        if response:
            assert all(isinstance(p, Player) for p in response)

    except AuthenticationError as e:
        pytest.fail(f"Authentication failed during test setup: {e}")
    except EsourceCommunicationError as e:
        pytest.fail(f"API communication error during test: {e}")
    except Exception as e:
        pytest.fail(f"An unexpected error occurred: {e}")


@pytest.mark.asyncio
@pytest.mark.integration
async def test_players_list_skip():
    """Tests the 'skip' query parameter offsets results."""
    try:
        session = AsyncSession(API_URL, TEST_EMAIL, TEST_PASSWORD)
        await session.login()

        players_resource = Players(session)

        first_player_list = await players_resource.list_players(take=1)
        if not first_player_list:
            pytest.skip("Cannot test skip: No players returned.")

        first_player_id = first_player_list[0].player_id

        second_player_list = await players_resource.list_players(skip=1, take=1)
        if not second_player_list:
            pytest.skip("Cannot test skip: Not enough players returned (need at least 2).")

        second_player_id = second_player_list[0].player_id

        assert first_player_id != second_player_id
        assert isinstance(second_player_list[0], Player)

    except AuthenticationError as e:
        pytest.fail(f"Authentication failed during test setup: {e}")
    except EsourceCommunicationError as e:
        pytest.fail(f"API communication error during test: {e}")
    except Exception as e:
        pytest.fail(f"An unexpected error occurred: {e}")


@pytest.mark.asyncio
@pytest.mark.integration
async def test_players_list_search():
    """Tests the 'search' query parameter filters results by name."""
    search_term = "Gabriel"

    try:
        session = AsyncSession(API_URL, TEST_EMAIL, TEST_PASSWORD)
        await session.login()

        players_resource = Players(session)
        response = await players_resource.list_players(search=search_term, take=10)

        assert isinstance(response, list)

        if not response:
            print(f"Warning: Search for '{search_term}' returned no players.")
        else:
            assert all(isinstance(p, Player) for p in response)
            for player in response:
                assert search_term.lower() in player.name.lower(), \
                    f"Player '{player.name}' (ID: {player.player_id}) found but doesn't match search '{search_term}'"

    except AuthenticationError as e:
        pytest.fail(f"Authentication failed during test setup: {e}")
    except EsourceCommunicationError as e:
        pytest.fail(f"API communication error during test: {e}")
    except Exception as e:
        pytest.fail(f"An unexpected error occurred: {e}")


@pytest.mark.asyncio
@pytest.mark.integration
async def test_players_list_orderby_id_asc():
    """Tests ordering players by player_id ascending."""
    try:
        session = AsyncSession(API_URL, TEST_EMAIL, TEST_PASSWORD)
        await session.login()

        players_resource = Players(session)
        response = await players_resource.list_players(order_by={"playerId": "asc"}, take=10)

        assert isinstance(response, list)
        if len(response) < 2:
            pytest.skip("Cannot verify sorting: Need at least 2 players returned.")

        assert all(isinstance(p, Player) for p in response)

        player_ids = [player.player_id for player in response]
        assert all(player_ids[i] <= player_ids[i + 1] for i in range(len(player_ids) - 1)), \
            f"List not sorted ascending by player_id: {id}"

    except AuthenticationError as e:
        pytest.fail(f"Authentication failed during test setup: {e}")
    except EsourceCommunicationError as e:
        pytest.fail(f"API communication error during test: {e}")
    except Exception as e:
        pytest.fail(f"An unexpected error occurred: {e}")


@pytest.mark.asyncio
@pytest.mark.integration
async def test_players_list_orderby_id_desc():
    """Tests ordering players by player_id descending."""
    try:
        session = AsyncSession(API_URL, TEST_EMAIL, TEST_PASSWORD)
        await session.login()

        players_resource = Players(session)
        response = await players_resource.list_players(order_by={"playerId": "desc"}, take=10)

        assert isinstance(response, list)
        if len(response) < 2:
            pytest.skip("Cannot verify sorting: Need at least 2 players returned.")

        assert all(isinstance(p, Player) for p in response)

        player_ids = [player.player_id for player in response]
        assert all(player_ids[i] >= player_ids[i + 1] for i in range(len(player_ids) - 1)), \
            f"List not sorted descending by player_id: {player_ids}"

    except AuthenticationError as e:
        pytest.fail(f"Authentication failed during test setup: {e}")
    except EsourceCommunicationError as e:
        pytest.fail(f"API communication error during test: {e}")
    except Exception as e:
        pytest.fail(f"An unexpected error occurred: {e}")
