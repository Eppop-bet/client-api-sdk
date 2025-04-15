from typing import List

from .base_resource import AsyncBaseResource
from .session import AsyncSession
from models.models import TradingTournament


class TradingTournaments(AsyncBaseResource):
    """Handles operations related to the /trading-tournaments endpoint."""
    def __init__(self, session: AsyncSession):
        super().__init__(session)
        self.base_url = "/trading-tournaments"

    async def list_trading_tournaments(
            self,
            skip=None,
            take=None,
            search=None,
            sport_id=None,
            trading_category_id=None) -> List[TradingTournament]:
        """
        Fetches a list of trading tournaments with optional pagination, search, sorting, and filtering.

        Args:
            skip (int, optional): Number of items to skip for pagination.
            take (int, optional): Number of items to take for pagination.
            search (str, optional): Search term for trading tournament names.
            sport_id (int or str, optional): Filter tournaments belonging to this sport ID.
            trading_category_id (int or str, optional): Filter tournaments belonging to this category ID.

        Returns:
            list: A list of trading tournament objects.
        """
        params = {}
        if sport_id is not None:
            params["sportId"] = sport_id
        if trading_category_id is not None:
            params["tradingCategoryId"] = trading_category_id

        params = self._build_common_params(params, skip=skip, take=take, order_by=None, search=search)

        data = await self.session.get(self.base_url, params=params)
        return [TradingTournament(**item) for item in data]

    async def get_trading_tournament(self, tournament_id) -> TradingTournament:
        """
        Fetches a single trading tournament by its ID.

        Args:
            tournament_id (int): The unique ID of the trading tournament.

        Returns:
            dict: The trading tournament details.
        """
        data = await self.get(tournament_id)
        return TradingTournament(**data)
