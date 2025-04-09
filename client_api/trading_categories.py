from .base_resource import BaseResource

class TradingCategory(BaseResource):
    """Handles operations related to the /trading-categories endpoint."""
    def __init__(self, session):
        super().__init__(session)
        self.base_url = "/trading-categories"

    def list_trading_categories(self, skip=None, take=None, search=None, sport_id=None, order_by=None):
        """
        Fetches a list of trading categories with optional pagination, search, sorting, and filtering by sport.

        Args:
            skip (int, optional): Number of items to skip for pagination.
            take (int, optional): Number of items to take for pagination.
            search (str, optional): Search term for trading category names.
            sport_id (int or str, optional): Filter categories belonging to this sport ID.
            order_by (str, optional): Field and direction to sort by (e.g., "name ASC").
                                      Note: Verify if API supports sorting on this endpoint.

        Returns:
            list: A list of trading category objects.
        """
        params = {}
        if sport_id is not None:
            params["sportId"] = sport_id

        params = self._build_common_params(params, skip=skip, take=take, order_by=order_by, search=search)

        return self.session.get(self.base_url, params=params)

    def get_trading_category(self, category_id):
        """
        Fetches a single trading category by its ID.

        Args:
            category_id (int): The unique ID of the trading category.

        Returns:
            dict: The trading category details.
        """
        return self.get(category_id)
