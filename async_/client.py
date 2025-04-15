from .changelog import Changelog
from .maps import Maps
from .players import Players
from .session import AsyncSession
from .sports import Sports
from .teams import Teams
from .trading_categories import TradingCategories
from .trading_events import TradingEvents
from .trading_tournaments import TradingTournaments


class AsyncClient:
    def __init__(self, base_url, email=None, password=None, session: AsyncSession = None):
        """
        Initializes the asynchronous client.

        Args:
            base_url (str): The base URL for the Esource API.
            email (str, optional): User email for login (stored for potential auto-login).
            password (str, optional): User password for login (stored for potential auto-login).
            session (AsyncSession, optional): An existing AsyncSession instance to use.
        """
        self.session = session or AsyncSession(base_url, email, password)

        self.sports = Sports(self.session)
        self.maps = Maps(self.session)
        self.players = Players(self.session)
        self.teams = Teams(self.session)
        self.changelog = Changelog(self.session)
        self.trading_events = TradingEvents(self.session)
        self.trading_tournaments = TradingTournaments(self.session)
        self.trading_categories = TradingCategories(self.session)

    async def login(self, email=None, password=None):
        """
        Asynchronously logs in using the provided credentials or stored credentials.

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
        return await self.session.login(email, password)

    async def __aenter__(self):
        """Enter async context management."""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Exit async context management, ensuring the session client is closed."""
        await self.session.close()

    async def close(self):
        """Closes the underlying session's HTTP client."""
        await self.session.close()
