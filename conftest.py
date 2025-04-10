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

    mock_request.return_value = mock_login_resp # Default response unless test overrides

    session = Session(base_url="http://mock-api.test/api", email="mock@user.com", password="mockpassword")

    session.token = login_response_data["AccessToken"]
    session._token_expiration_time = datetime.now(timezone.utc) + timedelta(seconds=login_response_data["ExpiresIn"] - 60)
    session.session.headers["Authorization"] = session.token

    yield session, mock_request

