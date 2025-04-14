from sync.changelog import Changelog
from sync.maps import Maps
from sync.players import Players
from sync.session import Session
from sync.sports import Sports
from sync.teams import Teams
from sync.trading_categories import TradingCategories
from sync.trading_events import TradingEvents
from sync.trading_tournaments import TradingTournaments


class SyncClient:
    def __init__(self, base_url, email=None, password=None, session: Session = None):
        self.session = session or Session(base_url, email, password)
        self.sports = Sports(self.session)
        self.maps = Maps(self.session)
        self.players = Players(self.session)
        self.teams = Teams(self.session)
        self.changelog = Changelog(self.session)
        self.trading_events = TradingEvents(self.session)
        self.trading_tournaments = TradingTournaments(self.session)
        self.trading_categories = TradingCategories(self.session)

    def login(self, email, password):
        return self.session.login(email, password)
