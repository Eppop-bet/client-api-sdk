from typing import List

from .base_resource import BaseResource
from .session import Session
from ..models.models import Map


class Maps(BaseResource):
    """Handles operations related to the /maps endpoint."""
    def __init__(self, session: Session):
        super().__init__(session)
        self.base_url = "v1/maps"

    def list_maps(self, skip=None, take=None, order_by=None, search=None) -> List[Map]:
        """
        Fetches a list of maps with optional pagination, sorting, and search.

        Args:
            skip (int, optional): Number of records to skip.
            take (int, optional): Number of records to retrieve.
            order_by (dict, optional): Field and direction to sort by. Example: {"name": "asc"} or {"name": "desc"}.
            search (str, optional): Search term for map names.

        Returns:
            list: A list of map objects.
        """
        params = self._build_common_params({}, skip=skip, take=take, order_by=order_by, search=search)
        data = self.session.get(self.base_url, params=params)
        return [Map(**item) for item in data]

    def get_map(self, map_id) -> Map:
        """
        Fetches a single map by its ID.

        Args:
            map_id (int): The unique ID of the map.

        Returns:
            dict: The map details.
        """
        data = self.get(map_id)
        return Map(**data)
