import pytest

from client_api.trading_categories import TradingCategories
from client_api.models import TradingCategory
from client_api.session import AuthenticationError, EsourceCommunicationError

from conftest import create_mock_response, CATEGORY_1, CATEGORY_2, CATEGORY_3


MOCK_CATEGORY_LIST_DATA = [CATEGORY_1, CATEGORY_2, CATEGORY_3]



def test_list_trading_categories_success(mock_session, mocker):
    session, mock_request = mock_session

    mock_api_resp = create_mock_response(mocker, 200, json_data=MOCK_CATEGORY_LIST_DATA)
    mock_request.return_value = mock_api_resp

    categories_resource = TradingCategories(session)
    result_categories = categories_resource.list_trading_categories()

    assert isinstance(result_categories, list)
    assert len(result_categories) == 3
    assert all(isinstance(c, TradingCategory) for c in result_categories)
    assert result_categories[0].id == 10
    assert result_categories[0].name == "Premier League"
    assert result_categories[1].id == 11
    assert result_categories[1].sportId == 3


def test_list_trading_categories_with_filters_success(mock_session, mocker):
    session, mock_request = mock_session

    mock_api_resp = create_mock_response(mocker, 200, json_data=MOCK_CATEGORY_LIST_DATA)
    mock_request.return_value = mock_api_resp

    categories_resource = TradingCategories(session)
    result_categories = categories_resource.list_trading_categories(
        sport_id=3,
        search="League",
        skip=0,
        take=5
    )

    assert isinstance(result_categories, list)
    assert len(result_categories) >= 0
    if result_categories:
        assert isinstance(result_categories[0], TradingCategory)


def test_get_trading_category_success(mock_session, mocker):
    session, mock_request = mock_session
    category_id_to_get = 10

    mock_api_resp = create_mock_response(mocker, 200, json_data=CATEGORY_1)
    mock_request.return_value = mock_api_resp

    categories_resource = TradingCategories(session)
    result_category = categories_resource.get_trading_category(category_id_to_get)

    assert isinstance(result_category, TradingCategory)
    assert result_category.id == category_id_to_get
    assert result_category.name == "Premier League"
    assert result_category.sportId == 3


def test_get_trading_category_not_found(mock_session, mocker):
    session, mock_request = mock_session
    category_id_to_get = 999

    mock_api_resp = create_mock_response(mocker, 404, text_data="Category Not Found")
    mock_request.return_value = mock_api_resp

    categories_resource = TradingCategories(session)

    with pytest.raises(EsourceCommunicationError) as excinfo:
        categories_resource.get_trading_category(category_id_to_get)
    assert "HTTP Error: 404 Not Found" in str(excinfo.value)


def test_list_trading_categories_auth_error(mock_session, mocker):
    session, mock_request = mock_session

    mock_api_resp = create_mock_response(mocker, 401, text_data="Unauthorized")
    mock_request.return_value = mock_api_resp

    categories_resource = TradingCategories(session)

    with pytest.raises(AuthenticationError):
        categories_resource.list_trading_categories()
