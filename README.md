# Esource.gg Python SDK

This is a Python SDK for interacting with the Esource.gg REST API (v1.0.0).
It provides a simple, consistent interface for authentication and accessing various API resources.

## Features

- Authenticated session management with automatic token refresh.
- Handles common API errors gracefully.
- Pythonic access to API resources:
    - Sports (`/sports`)
    - Maps (`/maps`)
    - Players (`/players`)
    - Teams (`/teams`, `/teams/{id}/players`)
    - Trading Categories (`/trading-categories`)
    - Trading Tournaments (`/trading-tournaments`)
    - Trading Events (`/trading-events`)
    - Changelog (`/changelog`)
- Support for common query parameters (`skip`, `limit`/`take`, `orderBy`, `search`) where applicable.
- Support for resource-specific query parameters (e.g., `timestamp`, `sportId`, `statuses`).
- Integration tested against the live API.
- Basic logging included.

## Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/<your_github_username>/<your_repo_name>.git
    cd <your_repo_name>
    ```

2.  **Install in editable mode (recommended for development):**
    ```bash
    pip install -e .
    ```
    *or for standard installation:*
    ```bash
    pip install .
    ```

3.  **Install development dependencies (for running tests):**
    ```bash
    pip install -r requirements-dev.txt
    ```
    *(You'll need to create a `requirements-dev.txt` containing `pytest` and potentially other dev tools)*

## Configuration

Integration tests require API credentials and the base API URL. Create a `.env` file in the project root directory:

```dotenv
# .env file
API_URL=https://esource.gg/api
TEST_EMAIL=your_test_email@example.com
TEST_PASSWORD=your_secret_password
```