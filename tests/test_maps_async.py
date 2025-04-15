import pytest
import httpx

from async_.maps import Maps
from async_.session import AsyncSession
from models.models import Map
from models.errors import AuthenticationError, EsourceCommunicationError

from conftest import MAP_1, MAP_2, MOCK_BASE_URL, MOCK_LOGIN_SUCCESS_DATA

MOCK_MAP_LIST_DATA = [MAP_1, MAP_2]


@pytest.mark.asyncio
async def test_list_maps_success(httpx_mock):
    httpx_mock.add_response(
        url=f"{MOCK_BASE_URL}/auth/sign-in",
        method="POST",
        json=MOCK_LOGIN_SUCCESS_DATA,
        status_code=200
    )
    httpx_mock.add_response(
        url=f"{MOCK_BASE_URL}/maps",
        method="GET",
        json=MOCK_MAP_LIST_DATA,
        status_code=200
    )

    async with AsyncSession(base_url=MOCK_BASE_URL) as session:
        await session.login(email="mock@user.com", password="mockpassword")
        maps_resource = Maps(session)

        result_maps = await maps_resource.list_maps()

        assert isinstance(result_maps, list)
        assert len(result_maps) == 2
        assert all(isinstance(m, Map) for m in result_maps)
        assert result_maps[0].map_id == 1
        assert result_maps[0].name == "Mirage"
        assert result_maps[1].map_id == 3
        assert result_maps[1].slug == "train"


@pytest.mark.asyncio
async def test_list_maps_with_params_success(httpx_mock):
    httpx_mock.add_response(
        url=f"{MOCK_BASE_URL}/auth/sign-in", method="POST", json=MOCK_LOGIN_SUCCESS_DATA, status_code=200
    )

    expected_params = {"skip": "10", "take": "5", "search": "Train", "orderBy": "name", "orderDir": "asc"}
    expected_url = httpx.URL(f"{MOCK_BASE_URL}/maps", params=expected_params)

    httpx_mock.add_response(
        url=expected_url,
        method="GET",
        json=[MAP_2],
        status_code=200
    )

    async with AsyncSession(base_url=MOCK_BASE_URL) as session:
        await session.login(email="mock@user.com", password="mockpassword")
        maps_resource = Maps(session)

        result_maps = await maps_resource.list_maps(skip=10, take=5, search="Train", order_by={"name": "asc"})

        assert isinstance(result_maps, list)
        assert len(result_maps) >= 0
        if result_maps:
            assert isinstance(result_maps[0], Map)
            assert result_maps[0].name == "Train"

        maps_request = httpx_mock.get_request(url=expected_url, method="GET")
        assert maps_request is not None
        assert maps_request.url.params == httpx.QueryParams(expected_params)


@pytest.mark.asyncio
async def test_get_map_success(httpx_mock):
    map_id_to_get = 1

    httpx_mock.add_response(
        url=f"{MOCK_BASE_URL}/auth/sign-in", method="POST", json=MOCK_LOGIN_SUCCESS_DATA, status_code=200
    )
    httpx_mock.add_response(
        url=f"{MOCK_BASE_URL}/maps/{map_id_to_get}",
        method="GET",
        json=MAP_1,
        status_code=200
    )

    async with AsyncSession(base_url=MOCK_BASE_URL) as session:
        await session.login(email="mock@user.com", password="mockpassword")
        maps_resource = Maps(session)

        result_map = await maps_resource.get_map(map_id_to_get)

        assert isinstance(result_map, Map)
        assert result_map.map_id == map_id_to_get
        assert result_map.name == "Mirage"
        assert result_map.slug == "mirage"


@pytest.mark.asyncio
async def test_get_map_not_found(httpx_mock):
    map_id_to_get = 999
    httpx_mock.add_response(
        url=f"{MOCK_BASE_URL}/auth/sign-in", method="POST", json=MOCK_LOGIN_SUCCESS_DATA, status_code=200
    )
    httpx_mock.add_response(
        url=f"{MOCK_BASE_URL}/maps/{map_id_to_get}",
        method="GET",
        text="Map Not Found",
        status_code=404
    )

    async with AsyncSession(base_url=MOCK_BASE_URL) as session:
        await session.login(email="mock@user.com", password="mockpassword")
        maps_resource = Maps(session)

        with pytest.raises(EsourceCommunicationError) as excinfo:
            await maps_resource.get_map(map_id_to_get)

        assert "HTTP Error: 404 Not Found" in str(excinfo.value)
        assert "Map Not Found" in str(excinfo.value)


@pytest.mark.asyncio
async def test_list_maps_auth_error(httpx_mock):
    httpx_mock.add_response(
        url=f"{MOCK_BASE_URL}/auth/sign-in", method="POST", json=MOCK_LOGIN_SUCCESS_DATA, status_code=200
    )
    httpx_mock.add_response(
        url=f"{MOCK_BASE_URL}/maps",
        method="GET",
        text="Unauthorized",
        status_code=401
    )

    async with AsyncSession(base_url=MOCK_BASE_URL) as session:
        await session.login(email="mock@user.com", password="mockpassword")
        maps_resource = Maps(session)

        with pytest.raises(AuthenticationError) as excinfo:
            await maps_resource.list_maps()

        assert "Unauthorized access (401)" in str(excinfo.value)
        assert "Unauthorized" in str(excinfo.value)
