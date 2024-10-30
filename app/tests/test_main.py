# test_main.py
import pytest
import json
import os
from app.main import save_to_json, fetch_and_save
from app.rick_and_morty_client import RickAndMortyClient


@pytest.mark.asyncio
async def test_save_to_json(tmp_path):
    """Test saving structured data to a JSON file."""
    data = [{"id": 1, "name": "Rick Sanchez"}]
    filename = tmp_path / "test_character.json"

    await save_to_json(data, filename)

    # Check if the file was created
    assert os.path.exists(filename)

    # Check file content
    with open(filename, "r") as f:
        content = json.load(f)
        assert "id" in content
        assert "RawData" in content
        assert content["RawData"] == data


@pytest.mark.asyncio
async def test_fetch_and_save(tmp_path, httpx_mock):
    """Test the full fetch and save functionality for 'episode'."""
    endpoint = "episode"
    filename = tmp_path / "test_episodes.json"
    start_year = 2017
    end_year = 2021

    # Mock data to return a single episode
    mock_data = {
        "info": {"next": None},
        "results": [
            {"id": 1, "name": "Mock Episode", "air_date": "June 20, 2017"}
        ]
    }

    # Mock the fetch_data response
    httpx_mock.add_response(url="https://rickandmortyapi.com/api/episode", json=mock_data)

    # Mock the client
    async with RickAndMortyClient() as client:
        await fetch_and_save(client, endpoint, filename, start_year=start_year, end_year=end_year)

    # Check file creation and contents
    assert os.path.exists(filename)
    with open(filename, "r") as f:
        content = json.load(f)
        assert "id" in content
        assert "RawData" in content
        assert content["RawData"] == mock_data["results"]
