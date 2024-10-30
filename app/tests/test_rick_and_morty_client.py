# test_rick_and_morty_client.py
import pytest
from app.rick_and_morty_client import RickAndMortyClient


@pytest.mark.asyncio
async def test_fetch_data(httpx_mock):
    """Test the basic fetch_data method of RickAndMortyClient with mock data."""
    mock_data = {"results": [{"id": 1, "name": "Mock Character"}]}
    url = "https://rickandmortyapi.com/api/character"

    # Mocking the response for a specific URL
    httpx_mock.add_response(url=url, json=mock_data)

    async with RickAndMortyClient() as client:
        response = await client.fetch_data(url)
        assert response["results"][0]["id"] == 1
        assert response["results"][0]["name"] == "Mock Character"


@pytest.mark.asyncio
async def test_fetch_all_data(httpx_mock):
    """Test fetching data from an endpoint with pagination."""
    endpoint = "character"
    mock_page_1 = {
        "info": {"next": "https://rickandmortyapi.com/api/character?page=2"},
        "results": [{"id": 1, "name": "Mock Character 1"}]
    }
    mock_page_2 = {
        "info": {"next": None},
        "results": [{"id": 2, "name": "Mock Character 2"}]
    }

    httpx_mock.add_response(url="https://rickandmortyapi.com/api/character", json=mock_page_1)
    httpx_mock.add_response(url="https://rickandmortyapi.com/api/character?page=2", json=mock_page_2)

    async with RickAndMortyClient() as client:
        data = await client.fetch_all_data(endpoint)
        assert len(data) == 2
        assert data[0]["id"] == 1
        assert data[1]["id"] == 2
