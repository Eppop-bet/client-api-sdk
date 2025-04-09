import requests
from datetime import datetime, timedelta, timezone
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class AuthenticationError(Exception):
    """Custom exception for authentication failures."""
    pass


class EsourceCommunicationError(Exception):
    """Custom exception for API communication errors."""
    pass


class Session:
    """
    Manages authentication and communication with the Esource API.

    Handles token acquisition, storage, automatic refresh, and making authenticated requests.
    """

    def __init__(self, base_url, email=None, password=None):
        """
        Initializes the session.

        Args:
            base_url (str): The base URL for the Esource API (e.g., "https://esource.gg/api").
            email (str, optional): The user's email for authentication. Defaults to None.
            password (str, optional): The user's password for authentication. Defaults to None.
        """
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.token = None
        self._token_expiration_time = None
        self._email = email
        self._password = password

        if email and password:
            try:
                self.login(email, password)
            except (AuthenticationError, EsourceCommunicationError) as e:
                logger.warning(f"Initial login failed during session creation: {e}")

    def login(self, email, password):
        """
        Authenticates with the API using email and password to obtain a token.

        Stores the token and its expiration time for subsequent requests.

        Args:
            email (str): The user's email.
            password (str): The user's password.

        Returns:
            dict: The JSON response from the sign-in endpoint.

        Raises:
            AuthenticationError: If login fails (invalid credentials, missing token in response).
            EsourceCommunicationError: If the request to the sign-in endpoint fails.
        """
        self._email = email
        self._password = password

        self.token = None
        self._token_expiration_time = None
        self.session.headers.pop("Authorization", None)

        try:
            response_json = self.post("/auth/sign-in", json={
                "email": email,
                "password": password
            })
        except EsourceCommunicationError as e:
            raise AuthenticationError(f"Login request failed: {e}") from e

        access_token = response_json.get("AccessToken")
        expires_in_seconds_val = response_json.get("ExpiresIn")

        if not access_token:
            raise AuthenticationError("Login failed: AccessToken not found in response.")

        if expires_in_seconds_val is not None:
            try:
                expires_in_seconds = int(expires_in_seconds_val)
                now = datetime.now(timezone.utc)
                buffer = timedelta(seconds=60)
                self._token_expiration_time = now + timedelta(seconds=expires_in_seconds) - buffer
                logger.info(f"Login successful. Token expires around: {self._token_expiration_time.isoformat()}")
            except (ValueError, TypeError):
                logger.warning(f"Could not parse 'ExpiresIn' value (expected seconds): {expires_in_seconds_val}. "
                               "Token expiration handling may not work.")
                self._token_expiration_time = None
        else:
            logger.warning("No 'ExpiresIn' value found in response. Token expiration cannot be tracked.")
            self._token_expiration_time = None

        self.token = access_token
        self.session.headers.update({"Authorization": self.token})

        return response_json

    def _is_token_expired(self):
        """Checks if the stored token is considered expired."""
        if not self.token or not self._token_expiration_time:
            # If no token or no expiration time, assume it needs login/refresh
            return True

        now = datetime.now(timezone.utc)
        return now >= self._token_expiration_time

    def _ensure_valid_token(self):
        """Ensures the session has a valid, non-expired token, attempting re-login if necessary."""
        token_was_expired = False
        if self._is_token_expired():
            if self.token:  # Only log if there was a token that actually expired
                logger.info(
                    f"Token expired or nearing expiry "
                    f"(expiry time: {self._token_expiration_time}), attempting re-login..."
                )
                token_was_expired = True

            self.token = None
            self._token_expiration_time = None
            self.session.headers.pop("Authorization", None)

            if self._email and self._password:
                try:
                    self.login(self._email, self._password)
                except (AuthenticationError, EsourceCommunicationError) as e:
                    if token_was_expired:
                        raise AuthenticationError(f"Failed to refresh expired token: {e}") from e
                    else:
                        raise AuthenticationError(f"Automatic login failed: {e}") from e
            else:
                if token_was_expired:
                    raise AuthenticationError("Token expired, but no credentials stored for automatic re-login.")
                else:
                    raise AuthenticationError("Not logged in and no credentials stored. Please call login() first.")

    def _request(self, method, path, needs_auth=True, **kwargs):
        """
        Internal method to make requests to the API. Handles token validation and errors.

        Args:
            method (str): HTTP method (GET, POST, PUT, DELETE).
            path (str): API endpoint path (e.g., "/sports").
            needs_auth (bool): Whether the endpoint requires authentication. Defaults to True.
            **kwargs: Additional arguments passed to requests.request (e.g., json, params).

        Returns:
            dict or str or None: The parsed JSON response, raw text, or None for 204 status.

        Raises:
            AuthenticationError: If authentication is required but fails or token expires.
            EsourceCommunicationError: For general request errors (network, HTTP status codes).
        """
        if needs_auth:
            self._ensure_valid_token()

        url = f"{self.base_url}/{path.lstrip('/')}"
        logger.debug(f"Requesting {method} {url} with params: {kwargs.get('params')}")

        try:
            response = self.session.request(method, url, **kwargs)
            response.raise_for_status()

            if response.status_code == 204:
                return None

            content_type = response.headers.get("Content-Type", "")
            if "application/json" in content_type:
                return response.json()
            else:
                logger.warning(f"Response from {url} is not JSON (Content-Type: {content_type}). Returning raw text.")
                return response.text

        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 401 and needs_auth:
                self.token = None
                self._token_expiration_time = None
                self.session.headers.pop("Authorization", None)
                logger.error("Authentication failed (401 Unauthorized). Check credentials or token.")
                raise AuthenticationError("Unauthorized access (401). Check credentials or token validity.") from e

            error_message = f"HTTP Error: {e.response.status_code} {e.response.reason} for url: {url}"
            try:
                error_details = e.response.json()
                error_message += f" Details: {error_details}"
            except requests.exceptions.JSONDecodeError:
                error_message += f" Response body: {e.response.text}"
            logger.error(error_message)
            raise EsourceCommunicationError(error_message) from e

        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed for {url}: {e}")
            raise EsourceCommunicationError(f"Request failed for {url}: {e}") from e

    def get(self, path, **kwargs):
        """Sends a GET request."""
        return self._request("GET", path, **kwargs)

    def post(self, path, needs_auth=False, **kwargs):
        """
        Sends a POST request.

        Note: Authentication is disabled by default for POST,
              as `/auth/sign-in` is the primary use case initially.
              Override `needs_auth=True` if other POST endpoints require it.
        """
        if path.endswith("/auth/sign-in"):
            needs_auth = False
        return self._request("POST", path, needs_auth=needs_auth, **kwargs)

    def put(self, path, **kwargs):
        """Sends a PUT request."""
        return self._request("PUT", path, **kwargs)

    def delete(self, path, **kwargs):
        """Sends a DELETE request."""
        return self._request("DELETE", path, **kwargs)
