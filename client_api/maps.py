from .base_resource import BaseResource


class Maps(BaseResource):
    """Handles operations related to the /maps endpoint."""
    def __init__(self, session):
        super().__init__(session)
        self.base_url = "/maps"

    def list_maps(self, skip=None, take=None, order_by=None, search=None):
        """
        Fetches a list of maps with optional pagination, sorting, and search.

        Args:
            skip (int, optional): Number of records to skip.
            take (int, optional): Number of records to retrieve. <--- Doc updated
            order_by (str, optional): Field and direction to sort by (e.g., "name ASC").
            search (str, optional): Search term for map names.

        Returns:
            list: A list of map objects.
        """
        return self.list(skip=skip, take=take, order_by=order_by, search=search)

    def get_map(self, map_id):
        """
        Fetches a single map by its ID.

        Args:
            map_id (int): The unique ID of the map.

        Returns:
            dict: The map details.
        """
        return self.get(map_id)
