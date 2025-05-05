from typing import List

from .base_resource import BaseResource
from .session import Session
from ..models.models import Sport


class Sports(BaseResource):
    """Handles operations related to the /sports endpoint."""
    def __init__(self, session: Session):
        super().__init__(session)
        self.base_url = "v1/sports"

    def list_sports(self, skip=None, take=None, order_by=None, search=None) -> List[Sport]:
        """
        Fetches a list of sports with optional pagination, sorting, and search.

        Args:
            skip (int, optional): Number of records to skip.
            take (int, optional): Number of records to retrieve.
            order_by (dict, optional): Field and direction to sort by. Example: {"name": "asc"} or {"name": "desc"}.
            search (str, optional): Search term for sport names.

        Returns:
            list: A list of sport objects.
        """
        params = self._build_common_params({}, skip=skip, take=take, order_by=order_by, search=search)
        data = self.session.get(self.base_url, params=params)
        return [Sport(**item) for item in data]

    def get_sport(self, sport_id) -> Sport:
        """
        Fetches a single sport by its ID.

        Args:
            sport_id (int): The unique ID of the sport.

        Returns:
            dict: The sport details.
        """
        data = self.get(sport_id)
        return Sport(**data)
