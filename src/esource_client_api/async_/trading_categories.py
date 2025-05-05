from typing import List

from .base_resource import AsyncBaseResource
from .session import AsyncSession
from ..models.models import TradingCategory


class TradingCategories(AsyncBaseResource):
    """Handles operations related to the /trading-categories endpoint."""
    def __init__(self, session: AsyncSession):
        super().__init__(session)
        self.base_url = "v1/trading-categories"

    async def list_trading_categories(self, skip=None, take=None, search=None, sport_id=None) -> List[TradingCategory]:
        """
        Fetches a list of trading categories with optional pagination, search, sorting, and filtering by sport.

        Args:
            skip (int, optional): Number of items to skip for pagination.
            take (int, optional): Number of items to take for pagination.
            search (str, optional): Search term for trading category names.
            sport_id (int or str, optional): Filter categories belonging to this sport ID.

        Returns:
            list: A list of trading category objects.
        """
        params = {}
        if sport_id is not None:
            params["sportId"] = sport_id

        params = self._build_common_params(params, skip=skip, take=take, order_by=None, search=search)

        data = await self.session.get(self.base_url, params=params)
        return [TradingCategory(**item) for item in data]

    async def get_trading_category(self, category_id) -> TradingCategory:
        """
        Fetches a single trading category by its ID.

        Args:
            category_id (int): The unique ID of the trading category.

        Returns:
            dict: The trading category details.
        """
        data = await self.get(category_id)
        return TradingCategory(**data)
