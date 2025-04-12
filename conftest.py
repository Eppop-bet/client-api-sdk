import pytest
import requests
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv
import os

from client_api.session import Session

load_dotenv()

API_URL = os.getenv("API_URL")
TEST_EMAIL = os.getenv("TEST_EMAIL")
TEST_PASSWORD = os.getenv("TEST_PASSWORD")

missing = []
if not API_URL:
    missing.append("API_URL")
if not TEST_EMAIL:
    missing.append("TEST_EMAIL")
if not TEST_PASSWORD:
    missing.append("TEST_PASSWORD")

if missing:
    raise RuntimeError(f"Missing required environment variables: {', '.join(missing)}")


def create_mock_response(mocker, status_code, json_data=None, text_data="", headers=None):
    mock_resp = mocker.Mock(spec=requests.Response)
    mock_resp.status_code = status_code
    mock_resp.json = mocker.Mock(return_value=json_data)
    mock_resp.text = text_data

    if headers is None:
        mock_resp.headers = {"Content-Type": "application/json"}
    else:
        mock_resp.headers = headers

    reason_map = {
        200: "OK",
        201: "Created",
        204: "No Content",
        400: "Bad Request",
        401: "Unauthorized",
        403: "Forbidden",
        404: "Not Found",
        500: "Internal Server Error",
    }
    mock_resp.reason = reason_map.get(status_code, "Unknown")

    if 400 <= status_code < 600:
        http_error = requests.exceptions.HTTPError(response=mock_resp)
        http_error.response = mock_resp
        mock_resp.raise_for_status = mocker.Mock(side_effect=http_error)
    else:
        mock_resp.raise_for_status = mocker.Mock()

    return mock_resp


@pytest.fixture
def mock_session(mocker):
    mock_request = mocker.patch('requests.Session.request', autospec=True)

    login_response_data = {
        "AccessToken": "mock-conftest-token-123",
        "ExpiresIn": 3600
    }
    mock_login_resp = create_mock_response(mocker, 200, json_data=login_response_data)

    mock_request.return_value = mock_login_resp  # Default response unless test overrides

    session = Session(base_url="http://mock-api.test/api", email="mock@user.com", password="mockpassword")

    session.token = login_response_data["AccessToken"]
    session._token_expiration_time = datetime.now(timezone.utc) + timedelta(
        seconds=login_response_data["ExpiresIn"] - 60)
    session.session.headers["Authorization"] = session.token

    yield session, mock_request


SPORT_1 = {"id": 3, "name": "Counter-Strike", "slug": "cs-go"}
SPORT_2 = {"id": 2, "name": "League of Legends", "slug": "lol"}

MAP_1 = {"mapId": 1, "name": "Mirage", "slug": "mirage"}
MAP_2 = {"mapId": 3, "name": "Train", "slug": "train"}

CATEGORY_1 = {"id": 10, "name": "Premier League", "sportId": 3}
CATEGORY_2 = {"id": 11, "name": "Champions League", "sportId": 3}
CATEGORY_3 = {"id": 20, "name": "World Championship", "sportId": 2}

TOURNAMENT_1 = {
    "id": 301, "name": "Major Championship", "sportId": 1, "tradingCategoryId": 10
}
TOURNAMENT_2 = {
    "id": 302, "name": "Regional Qualifier", "sportId": 1, "tradingCategoryId": None
}
TOURNAMENT_3 = {
    "id": 303, "name": "Another Game League", "sportId": 2, "tradingCategoryId": 20
}

PLAYER_1 = {
    "playerId": 101,
    "name": "Mock Player One",
    "firstName": "Mock",
    "lastName": "Player One",
    "active": True,
    "age": 25,
    "birthday": "1998-01-15T00:00:00Z",
    "imageUrl": "http://example.com/player1.jpg",
    "modifiedAt": "2023-10-26T10:00:00Z",
    "nationality": "Mocklandian",
    "role": "Test Role",
    "slug": "mock-player-one"
}

PLAYER_2 = {
    "playerId": 102,
    "name": "Mock Player Two",
    "firstName": "Mock",
    "lastName": "Player Two",
    "active": False,
    "age": None,
    "birthday": None,
    "imageUrl": None,
    "modifiedAt": "2023-10-27T11:00:00Z",
    "nationality": None,
    "role": None,
    "slug": "mock-player-two"
}

TEAM_1 = {
    "teamId": 201, "name": "Alpha Team", "slug": "alpha-team", "acronym": "AT",
    "imageUrl": "http://example.com/alpha.png", "location": "West", "modifiedAt": "2023-10-10T12:00:00Z"
}
TEAM_2 = {
    "teamId": 202, "name": "Bravo Team", "slug": "bravo-team", "acronym": "BT",
    "imageUrl": None, "location": "East", "modifiedAt": "2023-10-11T13:00:00Z"
}

TRADING_OUTCOME_1 = {
    "id": 1001, "name": "Team A Wins", "tradingMarketId": 201,
    "status": "Win", "result": "Win", "score": None, "price": 1.85, "probability": 0.50
}
TRADING_OUTCOME_2 = {
    "id": 1002, "name": "Team B Wins", "tradingMarketId": 201,
    "status": "Lose", "result": "Lose", "score": None, "price": 1.95, "probability": 0.48
}

TRADING_MARKET_1 = {
    "id": 201, "status": "Open", "eventId": 401, "period": "Map1",
    "competitorIds": [201, 202], "competitorType": "Team",
    "marketKey": "H2H", "value": None,
    "outcomes": [TRADING_OUTCOME_1, TRADING_OUTCOME_2]
}

TRADING_EVENT_1 = {
    "id": 401, "name": "Team A vs Team B - Grand Final", "sportId": 1,
    "sport": SPORT_1,
    "status": "Open",
    "beginAt": "2025-05-01T18:00:00Z", "modifiedAt": "2025-04-10T10:00:00Z",
    "archived": False, "notes": "Final match notes.",
    "competitorType": "Team", "competitorIds": [201, 202],
    "tradingMarkets": [TRADING_MARKET_1]
}
TRADING_EVENT_2 = {
    "id": 402, "name": "Player C vs Player D - Semifinal", "sportId": 1,
    "sport": SPORT_1,
    "status": "Suspended",
    "beginAt": "2025-05-01T16:00:00Z", "modifiedAt": "2025-04-10T09:00:00Z",
    "archived": False, "notes": None,
    "competitorType": "Player", "competitorIds": [601, 602],
    "tradingMarkets": []
}
