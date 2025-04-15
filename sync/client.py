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
    """
    Initializes the synchronous client.

    Args:
        base_url (str): The base URL for the Esource API.
        email (str, optional): User email for login (stored for potential auto-login).
        password (str, optional): User password for login (stored for potential auto-login).

            Client can be authenticated on init if email and password are not provided.
            Otherwise, call login() function to authenticate the client.
    """
    def __init__(self, base_url, email=None, password=None):
        self.session = Session(base_url, email, password)
        self.sports = Sports(self.session)
        self.maps = Maps(self.session)
        self.players = Players(self.session)
        self.teams = Teams(self.session)
        self.changelog = Changelog(self.session)
        self.trading_events = TradingEvents(self.session)
        self.trading_tournaments = TradingTournaments(self.session)
        self.trading_categories = TradingCategories(self.session)

    def login(self, email, password):
        """
        Synchronously logs in using the provided credentials or stored credentials.

        Args:
            email (str, optional): Email to use for login. Overrides stored email if provided.
            password (str, optional): Password to use for login. Overrides stored password if provided.

        Returns:
            SignInResponse: The response from the sign-in endpoint upon successful login.

        Raises:
            AuthenticationError: If login fails.
            EsourceCommunicationError: If the API request fails.
            ValueError: If email/password are not available.
        """
        return self.session.login(email, password)
