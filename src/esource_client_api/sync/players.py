from typing import List

from .base_resource import BaseResource
from ..models.models import Player


class Players(BaseResource):
    """Handles operations related to the /players endpoint."""
    def __init__(self, session):
        super().__init__(session)
        self.base_url = "/players"

    def list_players(self, skip=None, take=None, order_by=None, search=None) -> List[Player]:
        """
        Fetches a list of players with optional pagination, sorting, and search.

        Args:
            skip (int, optional): Number of records to skip.
            take (int, optional): Number of records to retrieve. <--- Doc updated
            order_by (dict, optional): Field and direction to sort by. Example: {"name": "asc"} or {"name": "desc"}.
            search (str, optional): Search term for player names.

        Returns:
            list: A list of player objects.
        """
        params = self._build_common_params({}, skip=skip, take=take, order_by=order_by, search=search)
        data = self.session.get(self.base_url, params=params)

        return [Player(**item) for item in data]

    def get_player(self, player_id) -> Player:
        """
        Fetches a single player by their ID.

        Args:
            player_id (int): The unique ID of the player.

        Returns:
            dict: The player details.
        """
        data = self.get(player_id)
        return Player(**data)
