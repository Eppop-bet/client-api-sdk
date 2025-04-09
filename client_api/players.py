from .base_resource import BaseResource

class Players(BaseResource):
    """Handles operations related to the /players endpoint."""
    def __init__(self, session):
        super().__init__(session)
        self.base_url = "/players"

    def list_players(self, skip=None, take=None, order_by=None, search=None):
        """
        Fetches a list of players with optional pagination, sorting, and search.

        Args:
            skip (int, optional): Number of records to skip.
            take (int, optional): Number of records to retrieve. <--- Doc updated
            order_by (str, optional): Field and direction to sort by (e.g., "name ASC").
            search (str, optional): Search term for player names.

        Returns:
            list: A list of player objects.
        """
        return self.list(skip=skip, take=take, order_by=order_by, search=search)

    def get_player(self, player_id):
        """
        Fetches a single player by their ID.

        Args:
            player_id (int): The unique ID of the player.

        Returns:
            dict: The player details.
        """
        return self.get(player_id)