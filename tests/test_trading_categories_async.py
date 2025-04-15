import httpx
import pytest

from async_.trading_categories import TradingCategories
from async_.session import AsyncSession
from conftest import MOCK_BASE_URL, MOCK_LOGIN_SUCCESS_DATA, CATEGORY_1
from models.models import TradingCategory
from models.errors import AuthenticationError, EsourceCommunicationError
from tests.test_trading_categories import MOCK_CATEGORY_LIST_DATA


@pytest.mark.asyncio
async def test_list_trading_categories_success(httpx_mock):
    """Test successfully listing trading categories."""
    httpx_mock.add_response(
        url=f"{MOCK_BASE_URL}/auth/sign-in", method="POST", json=MOCK_LOGIN_SUCCESS_DATA, status_code=200
    )
    httpx_mock.add_response(
        url=f"{MOCK_BASE_URL}/trading-categories", method="GET", json=MOCK_CATEGORY_LIST_DATA, status_code=200
    )

    async with AsyncSession(base_url=MOCK_BASE_URL) as session:
        await session.login(email="mock@user.com", password="mockpassword")
        categories_resource = TradingCategories(session)
        result_categories = await categories_resource.list_trading_categories()

        assert isinstance(result_categories, list)
        assert len(result_categories) == 3
        assert all(isinstance(c, TradingCategory) for c in result_categories)
        assert result_categories[0].id == 10
        assert result_categories[0].name == "Premier League"
        assert result_categories[1].id == 11
        assert result_categories[1].sport_id == 3


@pytest.mark.asyncio
async def test_list_trading_categories_with_filters_success(httpx_mock):
    """Test listing trading categories with filters."""
    httpx_mock.add_response(
        url=f"{MOCK_BASE_URL}/auth/sign-in", method="POST", json=MOCK_LOGIN_SUCCESS_DATA, status_code=200
    )

    expected_params = {"sportId": "3", "search": "League", "skip": "0", "take": "5"}
    expected_url = httpx.URL(f"{MOCK_BASE_URL}/trading-categories", params=expected_params)

    mock_filtered_data = [c for c in MOCK_CATEGORY_LIST_DATA if c["sportId"] == 3 and "League" in c["name"]]

    httpx_mock.add_response(
        url=str(expected_url),
        method="GET",
        json=mock_filtered_data,
        status_code=200
    )

    async with AsyncSession(base_url=MOCK_BASE_URL) as session:
        await session.login(email="mock@user.com", password="mockpassword")
        categories_resource = TradingCategories(session)
        result_categories = await categories_resource.list_trading_categories(
            sport_id=3,
            search="League",
            skip=0,
            take=5
        )

        assert isinstance(result_categories, list)
        assert len(result_categories) == len(mock_filtered_data)
        if result_categories:
            assert all(isinstance(c, TradingCategory) for c in result_categories)
            assert all(c.sport_id == 3 for c in result_categories)
            assert all("League" in c.name for c in result_categories)


@pytest.mark.asyncio
async def test_get_trading_category_success(httpx_mock):
    """Test successfully getting a single trading category."""
    category_id_to_get = 10
    httpx_mock.add_response(
        url=f"{MOCK_BASE_URL}/auth/sign-in", method="POST", json=MOCK_LOGIN_SUCCESS_DATA, status_code=200
    )
    httpx_mock.add_response(
        url=f"{MOCK_BASE_URL}/trading-categories/{category_id_to_get}",
        method="GET",
        json=CATEGORY_1,
        status_code=200
    )

    async with AsyncSession(base_url=MOCK_BASE_URL) as session:
        await session.login(email="mock@user.com", password="mockpassword")
        categories_resource = TradingCategories(session)
        result_category = await categories_resource.get_trading_category(category_id_to_get)

        assert isinstance(result_category, TradingCategory)
        assert result_category.id == category_id_to_get
        assert result_category.name == "Premier League"
        assert result_category.sport_id == 3


@pytest.mark.asyncio
async def test_get_trading_category_not_found(httpx_mock):
    """Test handling 404 when getting a trading category."""
    category_id_to_get = 999
    httpx_mock.add_response(
        url=f"{MOCK_BASE_URL}/auth/sign-in", method="POST", json=MOCK_LOGIN_SUCCESS_DATA, status_code=200
    )
    httpx_mock.add_response(
        url=f"{MOCK_BASE_URL}/trading-categories/{category_id_to_get}",
        method="GET",
        text="Category Not Found",
        status_code=404
    )

    async with AsyncSession(base_url=MOCK_BASE_URL) as session:
        await session.login(email="mock@user.com", password="mockpassword")
        categories_resource = TradingCategories(session)

        with pytest.raises(EsourceCommunicationError) as excinfo:
            await categories_resource.get_trading_category(category_id_to_get)

        assert "HTTP Error: 404 Not Found" in str(excinfo.value)
        assert "Category Not Found" in str(excinfo.value)


@pytest.mark.asyncio
async def test_list_trading_categories_auth_error(httpx_mock):
    """Test handling 401 when listing trading categories."""
    httpx_mock.add_response(
        url=f"{MOCK_BASE_URL}/auth/sign-in", method="POST", json=MOCK_LOGIN_SUCCESS_DATA, status_code=200
    )
    httpx_mock.add_response(
        url=f"{MOCK_BASE_URL}/trading-categories", method="GET", text="Unauthorized", status_code=401
    )

    async with AsyncSession(base_url=MOCK_BASE_URL) as session:
        await session.login(email="mock@user.com", password="mockpassword")
        categories_resource = TradingCategories(session)

        with pytest.raises(AuthenticationError) as excinfo:
            await categories_resource.list_trading_categories()

        assert "Unauthorized access (401)" in str(excinfo.value)
        assert "Unauthorized" in str(excinfo.value)
