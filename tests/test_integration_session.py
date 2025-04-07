from client_api.session import Session
from conftest import API_URL, TEST_EMAIL, TEST_PASSWORD


def test_real_login_sets_token_and_expiration():
    session = Session(API_URL, email=TEST_EMAIL, password=TEST_PASSWORD)

    assert session.token is not None
    assert session.expiration_time is not None

    assert session.session.headers.get("Authorization") == session.token