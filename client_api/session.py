from datetime import datetime, timedelta, timezone

import requests


class AuthenticationError(Exception):
    """Custom exception for authentication failure."""
    pass


class Session:
    def __init__(self, base_url, email=None, password=None):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.token = None
        self._token_expiration_time = None
        self._email = email
        self._password = password

        if email and password:
            try:
                self.login(email, password)
            except Exception as e:
                print(f"Warning: Initial login failed during session creation: {e}")

    def login(self, email, password):
        self._email = email
        self._password = password

        self.token = None
        self._token_expiration_time = None
        self.session.headers.pop("Authorization", None)

        response = self.post("/auth/sign-in", json={
            "email": email,
            "password": password
        })

        access_token = response.get("AccessToken")
        expires_in_ms = response.get("ExpiresIn")

        if not access_token:
            raise AuthenticationError(
                "Login failed: AccessToken not found in response"
            )
        else:
            try:
                expires_in_seconds = int(expires_in_ms) / 1000.0
                now = datetime.now(timezone.utc)
                self._token_expiration_time = now + timedelta(seconds=expires_in_seconds)
            except (ValueError, TypeError):
                print(f"Warning: Could not parse 'ExpiresIn' value (expected ms): {expires_in_ms}. "
                      "Token expiration handling may not work.")
                self._token_expiration_time = None

        self.token = access_token
        self.session.headers.update({"Authorization": self.token})

        if self._token_expiration_time:
            print(f"Login successful. Token expires at: {self._token_expiration_time.isoformat()}")

        return response

    def _is_token_expired(self):
        """Checks if the token"s exact expiration time has passed."""
        if not self.token or not self._token_expiration_time:
            return False

        # Use UTC for comparison
        now = datetime.now(timezone.utc)
        return now >= self._token_expiration_time

    def _ensure_valid_token(self):
        """Ensures the session has a valid, non-expired token."""
        token_was_expired = False
        if self.token and self._is_token_expired():
            print(
                f"Token expired at {self._token_expiration_time.isoformat()}, attempting re-login..."
            )
            token_was_expired = True
            self.token = None
            self._token_expiration_time = None
            self.session.headers.pop("Authorization", None)

        if not self.token:
            if self._email and self._password:
                try:
                    self.login(self._email, self._password)
                except Exception as e:
                    if token_was_expired:
                        raise AuthenticationError(f"Failed to refresh expired token: {e}") from e
                    else:
                        raise AuthenticationError(f"Automatic login failed: {e}") from e
            else:
                if token_was_expired:
                    raise AuthenticationError(
                        "Token expired, but no credentials stored for automatic re-login."
                    )
                else:
                    raise AuthenticationError(
                        "Not logged in and no credentials stored. Please call login() first."
                    )

    def _request(self, method, path, **kwargs):
        self._ensure_valid_token()

        url = f"{self.base_url}/{path.lstrip("/")}"
        try:
            response = self.session.request(method, url, **kwargs)
            response.raise_for_status()

            if response.status_code == 204:
                return None

            if "application/json" in response.headers.get("Content-Type", ""):
                return response.json()
            else:
                return response.text

        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 401:
                self.token = None
                self._token_expiration_time = None
                self.session.headers.pop("Authorization", None)
                raise AuthenticationError(
                    "Unauthorized access. Check credentials or permissions."
                ) from e

            print(f"HTTP Error occurred: {e.response.status_code} {e.response.reason}")
            try:
                error_details = e.response.json()
                print(f"Error details: {error_details}")
            except requests.exceptions.JSONDecodeError:
                print(f"Error response body: {e.response.text}")
            raise
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            raise

    def get(self, path, **kwargs):
        return self._request("GET", path, **kwargs)

    def post(self, path, **kwargs):
        return self._request("POST", path, **kwargs)

    def put(self, path, **kwargs):
        return self._request("PUT", path, **kwargs)

    def delete(self, path, **kwargs):
        return self._request("DELETE", path, **kwargs)
