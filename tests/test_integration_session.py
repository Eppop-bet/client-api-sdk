import pytest
from datetime import datetime, timezone
from client_api.session import Session, AuthenticationError
from conftest import API_URL, TEST_EMAIL, TEST_PASSWORD


def test_real_login_sets_token_and_expiration():
    """Tests successful login sets token and expiration time."""
    session = Session(API_URL, email=TEST_EMAIL, password=TEST_PASSWORD)

    assert session.token is not None
    assert session._token_expiration_time is not None
    assert isinstance(session._token_expiration_time, datetime)
    assert session._token_expiration_time > datetime.now(timezone.utc)
    assert session.session.headers.get("Authorization") == session.token


def test_login_failure_raises_exception():
    """Tests that login with invalid credentials raises AuthenticationError."""
    with pytest.raises(AuthenticationError):
        Session(API_URL, email=TEST_EMAIL, password="wrongpassword")
