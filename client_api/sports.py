from .base_resource import BaseResource


class Sports(BaseResource):
    """Handles operations related to the /sports endpoint."""
    def __init__(self, session):
        super().__init__(session)
        self.base_url = "/sports"

    def list_sports(self, skip=None, take=None, order_by=None, search=None):
        """
        Fetches a list of sports with optional pagination, sorting, and search.

        Args:
            skip (int, optional): Number of records to skip.
            take (int, optional): Number of records to retrieve. <--- Doc updated
            order_by (str, optional): Field and direction to sort by (e.g., "name ASC").
            search (str, optional): Search term for sport names.

        Returns:
            list: A list of sport objects.
        """
        return self.list(skip=skip, take=take, order_by=order_by, search=search)

    def get_sport(self, sport_id):
        """
        Fetches a single sport by its ID.

        Args:
            sport_id (int): The unique ID of the sport.

        Returns:
            dict: The sport details.
        """
        return self.get(sport_id)
