from typing import List

from .base_resource import BaseResource
from .session import Session
from ..models.models import TradingEvent


class TradingEvents(BaseResource):
    """Handles operations related to the /trading-events endpoint."""
    def __init__(self, session: Session):
        super().__init__(session)
        self.base_url = "v1/trading-events"

    def list_trading_events(
            self,
            skip=None,
            take=None,
            search=None,
            sport_id=None,
            trading_tournament_id=None,
            statuses=None) -> List[TradingEvent]:
        """
        Fetches a list of trading events with optional pagination, search, sorting, and filtering.

        Args:
            skip (int, optional): Number of items to skip for pagination.
            take (int, optional): Number of items to take for pagination.
            search (str, optional): Search term for trading event names.
            sport_id (int or str, optional): Filter events belonging to this sport ID.
            trading_tournament_id (int or str, optional): Filter events belonging to this tournament ID.
            statuses (str, optional): Comma-separated string of statuses to filter by (e.g., "Open,Suspended").

        Returns:
            list: A list of trading event objects.
        """
        params = {}
        if sport_id is not None:
            params["sportId"] = sport_id
        if trading_tournament_id is not None:
            params["tradingTournamentId"] = trading_tournament_id
        if statuses:
            params["statuses"] = statuses

        params = self._build_common_params(params, skip=skip, take=take, order_by=None, search=search)

        data = self.session.get(self.base_url, params=params)
        return [TradingEvent(**item) for item in data]

    def get_trading_event(self, event_id) -> TradingEvent:
        """
        Fetches a single trading event by its ID.

        Args:
            event_id (int): The unique ID of the trading event.

        Returns:
            dict: The trading event details, potentially including markets and outcomes.
        """
        data = self.get(event_id)
        return TradingEvent(**data)
