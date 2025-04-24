# Esource.gg Python SDK

This is a Python SDK for interacting with the Esource.gg REST API.
It provides a simple, consistent interface for authentication and accessing various API resources using both synchronous and asynchronous programming paradigms.

## Features

-   Authenticated session management with automatic token refresh.
-   Handles common API errors gracefully (`AuthenticationError`, `EsourceCommunicationError`).
-   Provides both synchronous (`SyncClient`) and asynchronous (`AsyncClient`) clients.
-   Pythonic access to API resources with Pydantic models for data validation:
    -   Sports (`/sports`)
    -   Maps (`/maps`)
    -   Players (`/players`)
    -   Teams (`/teams`, `/teams/{id}/players`)
    -   Trading Categories (`/trading-categories`)
    -   Trading Tournaments (`/trading-tournaments`)
    -   Trading Events (`/trading-events`)
    -   Changelog (`/changelog`)
-   Support for common query parameters (`skip`, `take`, `orderBy`, `search`) where applicable.
-   Support for resource-specific query parameters (e.g., `timestamp`, `sportId`, `statuses`).
-   Reliable and tested implementation.

## Installation

Install the package directly from PyPI:

```bash
pip install esource-client-api
```

## Authentication
To use the API, you need valid credentials (email and password) and the base URL of the Esource API (obtainable from Esource.gg documentation or support).

You can authenticate either when initializing the client or by calling the `login()` method afterwards.
Provide credentials during initialization

```bash
client = SyncClient(API_BASE_URL, email="your_email", password="your_password")
```

Or initialize first, then login

```bash
client = SyncClient(API_BASE_URL)
client.login("your_email", "your_password")
```

The same applies to the AsyncClient.

## Basic Usage
### Synchronous Client (SyncClient)

```bash
from esource_client_api.sync import SyncClient
from esource_client_api.models.errors import AuthenticationError, EsourceCommunicationError
```

Replace with your actual API base URL and credentials

```python
API_BASE_URL = "https://esource.gg/api"
EMAIL = "your_email@example.com"
PASSWORD = "your_password"

try:
    # Initialize and log in automatically
    client = SyncClient(API_BASE_URL, email=EMAIL, password=PASSWORD)
    # Alternatively:
    # client = SyncClient(API_BASE_URL)
    # client.login(EMAIL, PASSWORD)

    print("Login successful!")

    # Example: List the first 5 sports
    sports_list = client.sports.list_sports(take=5)
    print("\nAvailable Sports (first 5):")
    for sport in sports_list:
        print(f"- {sport.name} (ID: {sport.id}, Slug: {sport.slug})")

    # Example: Get a specific player by ID (replace with a valid ID)
    try:
        player = client.players.get_player(17497)
        print(f"\nPlayer Details (ID 17497): {player.name}")
    except EsourceCommunicationError as e:
        print(f"\nCould not get player 17497: {e}")


except AuthenticationError as e:
    print(f"Authentication failed: {e}")
except EsourceCommunicationError as e:
    print(f"API communication error: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
```


## Asynchronous Client (AsyncClient)
Using asyncio and the AsyncClient requires an async context.
Authorizing AsyncClient has to be done through invoking `login()` methond and cannot be done during class initialization.

```python
from esource_client_api.async_ import AsyncClient
from esource_client_api.models.errors import AuthenticationError, EsourceCommunicationError

# Replace with your actual API base URL and credentials
API_BASE_URL = "https://esource.gg/api"
EMAIL = "your_email@example.com"
PASSWORD = "your_password"

async def main():
    # Using the client as an async context manager handles session closing
    async with AsyncClient(API_BASE_URL) as client:
        try:
            # Log in
            await client.login(EMAIL, PASSWORD)
            print("Async login successful!")

            # Example: List the first 5 maps asynchronously
            maps_list = await client.maps.list_maps(take=5)
            print("\nAvailable Maps (first 5):")
            for map_item in maps_list:
                print(f"- {map_item.name} (ID: {map_item.map_id}, Slug: {map_item.slug})")

            # Example: Get a specific team by ID asynchronously (replace with a valid ID)
            try:
                team = await client.teams.get_team(13444)
                print(f"\nTeam Details (ID 13444): {team.name}")
            except EsourceCommunicationError as e:
                print(f"\nCould not get team 13444: {e}")


        except AuthenticationError as e:
            print(f"Authentication failed: {e}")
        except EsourceCommunicationError as e:
            print(f"API communication error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    # Required to run the async main function
    asyncio.run(main())
```

## Available Resources

Once the client is initialized and authenticated, you can access the different API resources via the client's attributes:

-   `client.sports`: Access sports data.
-   `client.maps`: Access map data.
-   `client.players`: Access player data.
-   `client.teams`: Access team data, including players per team.
-   `client.trading_categories`: Access trading category data.
-   `client.trading_tournaments`: Access trading tournament data.
-   `client.trading_events`: Access trading event data, including markets and outcomes.
-   `client.changelog`: Access the changelog for data updates.

Refer to the method docstrings within the SDK or the official Esource API documentation for details on available methods and parameters for each resource (e.g., `list_sports()`, `get_player(player_id)`, `list_trading_events(sport_id=...)`).

## API URL & Docs

URL to interact with the API: https://esource.gg/api/

Swagger Docs for Api are available here: https://esource.gg/api/docs/

Please contact support for access.

## License

This SDK is distributed under the MIT License. See the `LICENSE` file for more details.

## Support & Source Code

For issues or questions regarding the SDK, please refer to the [GitHub repository](https://github.com/Eppop-bet/client-api-sdk).
