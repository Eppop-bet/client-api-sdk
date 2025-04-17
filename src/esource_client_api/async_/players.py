from typing import List

from .base_resource import AsyncBaseResource
from .session import AsyncSession
from ..models.models import Player


class Players(AsyncBaseResource):
    """Handles operations related to the /players endpoint."""
    def __init__(self, session: AsyncSession):
        super().__init__(session)
        self.base_url = "/players"

    async def list_players(self, skip=None, take=None, order_by=None, search=None) -> List[Player]:
        """
        Fetches a list of players with optional pagination, sorting, and search.

        Args:
            skip (int, optional): Number of records to skip.
            take (int, optional): Number of records to retrieve.
            order_by (dict, optional): Field and direction to sort by. Example: {"name": "asc"} or {"name": "desc"}.
            search (str, optional): Search term for player names.

        Returns:
            list: A list of player objects.
        """
        params = self._build_common_params({}, skip=skip, take=take, order_by=order_by, search=search)
        data = await self.session.get(self.base_url, params=params)
        return [Player(**item) for item in data]

    async def get_player(self, player_id) -> Player:
        """
        Fetches a single player by their ID.

        Args:
            player_id (int): The unique ID of the player.

        Returns:
            dict: The player details.
        """
        data = await self.get(player_id)
        return Player(**data)
