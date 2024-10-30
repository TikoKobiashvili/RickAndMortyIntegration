# app/tests/test_main.py
import json
import os
import pytest
from unittest.mock import patch
from app.main import save_to_json, fetch_episode_names_in_date_range, fetch_and_save
from app.rick_and_morty_client import RickAndMortyClient


# Create a mock class for RickAndMortyClient to use in tests
class MockRickAndMortyClient:
    """Mocking the RickAndMortyClient for testing."""

    async def fetch_all_data(self, entity):
        """Mocked method to return data based on entity."""
        if entity == "character":
            return [{"id": 1, "name": "Rick Sanchez"}]
        elif entity == "location":
            return [{"id": 1, "name": "Earth (C-137)"}]
        elif entity == "episode":
            return [
                {"id": 1, "name": "Pilot", "air_date": "December 2, 2013"},
                {"id": 2, "name": "The Ricklantis Mixup", "air_date": "September 10, 2017"},
                {"id": 3, "name": "The Old Man and the Seat", "air_date": "November 17, 2019"},
                {"id": 4, "name": "Mort Dinner Rick Andre", "air_date": "June 20, 2021"},
                {"id": 5, "name": "Forgetting Sarick Mortshall", "air_date": "September 5, 2021"}
            ]
        return []


@pytest.mark.asyncio
async def test_save_to_json(tmp_path):
    """Test saving structured data to a JSON file in a temporary directory."""
    data = [{"id": 1, "name": "Rick Sanchez"}]
    entity = "test_character"

    # Use the temporary results directory provided by pytest
    results_dir = tmp_path / "results"
    os.makedirs(results_dir, exist_ok=True)

    # Mock the save_to_json function to save to the tmp directory
    with patch('app.main.RESULTS_DIR', results_dir):
        await save_to_json(data, entity)

    # Construct expected filename
    expected_filename = os.path.join(results_dir, f'{entity}.json')

    # Check if the file was created
    assert os.path.exists(expected_filename)

    # Check file content
    with open(expected_filename, "r") as f:
        content = json.load(f)
        assert "id" in content
        assert "RawData" in content
        assert content["RawData"] == data


@pytest.mark.asyncio
async def test_fetch_and_save(tmp_path):
    """Test the full fetch and save functionality for 'episode'."""
    endpoint = "episode"
    start_year = 2017
    end_year = 2021

    # Use the temporary results directory
    results_dir = tmp_path / "results"
    os.makedirs(results_dir, exist_ok=True)

    # Use the mocked client
    client = MockRickAndMortyClient()

    # Mocking save_to_json to save to tmp_path
    with patch('app.main.RESULTS_DIR', results_dir):
        await fetch_and_save(client, endpoint, start_year=start_year, end_year=end_year)

    # Construct expected filename
    expected_filename = os.path.join(results_dir, "episode.json")

    # Check file creation and contents
    assert os.path.exists(expected_filename)

    with open(expected_filename, "r") as f:
        content = json.load(f)
        assert "id" in content
        assert "RawData" in content

        # Await the fetch_all_data call to get the actual data
        expected_data = await client.fetch_all_data(endpoint)
        assert content["RawData"] == expected_data
