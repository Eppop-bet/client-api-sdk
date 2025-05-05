import httpx
from datetime import datetime, timedelta, timezone
import logging
from typing import Optional

from ..models.models import SignInResponse
from ..models.errors import AuthenticationError, EsourceCommunicationError


logger = logging.getLogger(__name__)


class AsyncSession:
    """
    Manages async_ authentication and communication with the Esource API using httpx.

    Handles token acquisition, storage, automatic refresh, and making authenticated requests.
    """

    def __init__(self, base_url: str, email: Optional[str] = None, password: Optional[str] = None):
        """
        Initializes the async_ session. Does NOT automatically login. Call login() separately.

        Args:
            base_url (str): The base URL for the Esource API (e.g., "https://esource.gg/api").
            email (str, optional): The user's email for authentication (stored for potential re-login).
            password (str, optional): The user's password for authentication (stored for potential re-login).
        """
        self.base_url = base_url.rstrip("/")
        self.client = httpx.AsyncClient(base_url=self.base_url, follow_redirects=True)
        self.token: Optional[str] = None
        self._token_expiration_time: Optional[datetime] = None
        self._email = email
        self._password = password

    async def login(self, email: Optional[str] = None, password: Optional[str] = None) -> SignInResponse:
        """
        Asynchronously authenticates with the API using email/password to obtain a token.

        Stores the token and its expiration time for subsequent requests.
        Uses provided credentials or falls back to credentials provided during init.

        Args:
            email (str, optional): The user's email. Overrides email from init if provided.
            password (str, optional): The user's password. Overrides password from init if provided.

        Returns:
            SignInResponse: Pydantic model of the sign-in response.

        Raises:
            AuthenticationError: If login fails (invalid credentials, missing token in response).
            EsourceCommunicationError: If the request to the sign-in endpoint fails.
            ValueError: If email or password are not available.
        """
        login_email = email or self._email
        login_password = password or self._password

        if not login_email or not login_password:
            raise ValueError("Email and password must be provided either during init or to login().")

        self._email = login_email
        self._password = login_password

        self.token = None
        self._token_expiration_time = None
        self.client.headers.pop("Authorization", None)

        try:
            response_json = await self._request(
                "POST",
                "v1/auth/sign-in",
                needs_auth=False,
                json={
                    "email": login_email,
                    "password": login_password
                }
            )
            if response_json is None:
                raise AuthenticationError("Login failed: Received empty response from server.")

            sign_in_data = SignInResponse(**response_json)

        except EsourceCommunicationError as e:
            raise AuthenticationError(f"Login request failed: {e}") from e
        except Exception as e:
            if isinstance(e, AuthenticationError):
                raise
            raise AuthenticationError(f"Login failed during response processing: {e}") from e

        access_token = sign_in_data.access_token
        expires_in_seconds = sign_in_data.expires_in

        now = datetime.now(timezone.utc)
        buffer = timedelta(seconds=60)
        try:
            self._token_expiration_time = now + timedelta(seconds=expires_in_seconds) - buffer
            logger.info(f"Async login successful. Token expires around: {self._token_expiration_time.isoformat()}")
        except TypeError:
            logger.warning(f"Could not calculate expiration time from ExpiresIn: {expires_in_seconds}. "
                           "Token expiration handling may not work.")
            self._token_expiration_time = None

        self.token = access_token
        self.client.headers.update({"Authorization": self.token})

        return sign_in_data

    def _is_token_expired(self) -> bool:
        """Checks if the stored token is considered expired."""
        if not self.token or not self._token_expiration_time:
            return True

        now = datetime.now(timezone.utc)
        return now >= self._token_expiration_time

    async def _ensure_valid_token(self):
        """
        Ensures the session has a valid, non-expired token, attempting async_ re-login if necessary.
        """
        token_was_expired = False
        if self._is_token_expired():
            if self.token:
                logger.info(
                    f"Async token expired or nearing expiry "
                    f"(expiry time: {self._token_expiration_time}), attempting re-login..."
                )
                token_was_expired = True

            self.token = None
            self._token_expiration_time = None
            self.client.headers.pop("Authorization", None)

            if self._email and self._password:
                logger.info(f"Attempting automatic async_ re-login for {self._email}")
                try:
                    await self.login(self._email, self._password)
                    logger.info("Automatic async_ re-login successful.")
                except (AuthenticationError, EsourceCommunicationError, ValueError) as e:
                    error_msg = f"Failed to refresh expired token: {e}" \
                        if token_was_expired else f"Automatic async_ login failed: {e}"
                    logger.error(error_msg)
                    raise AuthenticationError(error_msg) from e
            else:
                error_msg = "Token expired, but no credentials stored for automatic re-login." \
                    if token_was_expired else "Not logged in and no credentials stored. Please call login() first."
                logger.warning(error_msg)
                raise AuthenticationError(error_msg)

    async def _request(self, method: str, path: str, needs_auth: bool = True, **kwargs):
        """
        Internal async_ method to make requests to the API using httpx.AsyncClient.

        Handles token validation, errors, and response parsing.

        Args:
            method (str): HTTP method (GET, POST, PUT, DELETE).
            path (str): API endpoint path (e.g., "/sports").
            needs_auth (bool): Whether the endpoint requires authentication. Defaults to True.
            **kwargs: Additional arguments passed to httpx.AsyncClient.request (e.g., json, params).

        Returns:
            dict or str or None: The parsed JSON response, raw text, or None for 204 status.

        Raises:
            AuthenticationError: If authentication is required but fails or token expires.
            EsourceCommunicationError: For general request errors (network, HTTP status codes).
        """
        if needs_auth:
            await self._ensure_valid_token()

        relative_url = path.lstrip('/')
        logger.debug(f"Async requesting {method} {relative_url} with params: {kwargs.get('params')}")

        try:
            response = await self.client.request(method, relative_url, **kwargs)
            response.raise_for_status()

            if response.status_code == 204:
                return None

            content_type = response.headers.get("Content-Type", "")
            if "application/json" in content_type:
                return response.json()
            else:
                logger.warning(
                    f"Response from {relative_url} is not JSON (Content-Type: {content_type}). Returning raw text.")
                return response.text

        except httpx.HTTPStatusError as e:
            if e.response.status_code == 401 and needs_auth:
                self.token = None
                self._token_expiration_time = None
                self.client.headers.pop("Authorization", None)
                logger.error("Async authentication failed (401 Unauthorized). Check credentials or token.")
                details = e.response.text
                raise AuthenticationError(
                    f"Unauthorized access (401). Check credentials or token validity. Details: {details}") from e

            error_message = f"HTTP Error: {e.response.status_code} {e.response.reason_phrase} for url: {e.request.url}"
            try:
                error_details = e.response.json()
                error_message += f" Details: {error_details}"
            except Exception:
                error_message += f" Response body: {e.response.text}"

            logger.error(error_message)
            raise EsourceCommunicationError(error_message) from e

        except httpx.RequestError as e:
            logger.error(f"Async request failed for {e.request.url}: {e}")
            raise EsourceCommunicationError(f"Request failed for {e.request.url}: {e}") from e
        except Exception as e:
            logger.error(f"An unexpected error occurred during async_ request to {relative_url}: {e}")
            if isinstance(e, (AuthenticationError, EsourceCommunicationError)):
                raise
            raise EsourceCommunicationError(f"An unexpected error occurred: {e}") from e

    async def get(self, path: str, **kwargs):
        """Sends an async_ GET request."""
        return await self._request("GET", path, **kwargs)

    async def post(self, path: str, needs_auth: bool = True, **kwargs):
        """
        Sends an async_ POST request. Defaults to requiring auth, unlike sync version.
        Override needs_auth=False for endpoints like /auth/sign-in.
        """
        return await self._request("POST", path, needs_auth=needs_auth, **kwargs)

    async def put(self, path: str, **kwargs):
        """Sends an async_ PUT request."""
        return await self._request("PUT", path, **kwargs)

    async def delete(self, path: str, **kwargs):
        """Sends an async_ DELETE request."""
        return await self._request("DELETE", path, **kwargs)

    async def close(self):
        """Closes the underlying httpx client. Recommended to call when done."""
        await self.client.aclose()
        logger.info("Async HTTP client closed.")

    async def __aenter__(self):
        """Enter async context management."""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Exit async context management, ensuring client closure."""
        await self.close()
