# main.py
import asyncio
import json
import os
import uuid
from datetime import datetime
from app.rick_and_morty_client import RickAndMortyClient

RESULTS_DIR = os.path.join(os.path.dirname(__file__), "..", "results")
os.makedirs(RESULTS_DIR, exist_ok=True)


async def save_to_json(data, entity):
    """
    Save the fetched data to a JSON file with a structured format.
    Parameters:
        data (list): The data to save.
        entity (str): The name of the JSON file.
    """
    structured_data = {
        "id": str(uuid.uuid4()),  # Generate a unique ID
        "RawData": data  # Store the original API response
    }
    # Create the full path for the JSON file
    full_path = os.path.join(RESULTS_DIR, f'{entity}.json')
    # Write data to a JSON file with indentation for readability
    with open(full_path, "w") as f:
        json.dump(structured_data, f, indent=4)


async def fetch_episode_names_in_date_range(episodes, start_year, end_year):
    """
    Fetch all episode names that aired within a specified year range.
    Parameters:
        episodes (list): List of all the episodes.
        start_year (int): The starting year of the date range.
        end_year (int): The ending year of the date range.
    Prints:
        list: List of episode names within the specified date range.
    """
    # Filter episodes by air date within the specified range
    filtered_episodes = [
        ep['name'] for ep in episodes
        if start_year <= datetime.strptime(ep['air_date'], '%B %d, %Y').year <= end_year
    ]
    if filtered_episodes:
        print(f"Episodes aired between {start_year} and {end_year}:", filtered_episodes)
    else:
        print(f"There are no episodes that aired between {start_year} and {end_year}:")


async def fetch_and_save(client, entity, start_year=None, end_year=None):
    """
    Fetch data for a specific entity and save it to a JSON file.
    Parameters:
        client (RickAndMortyClient): The client instance to fetch data.
        entity (str): The type of entity (e.g., 'character', 'location', 'episode').
        filename (str): The name of the file to save data to.
        end_year (int): if entity is episodes, end year of the range for printing episode names
        start_year (int): if entity is episodes, start year of the range for printing episode names
    """
    # Fetch data using the appropriate client method
    data = await client.fetch_all_data(entity)
    # Print episode names on given year range
    if entity == "episode":
        await fetch_episode_names_in_date_range(data, start_year=start_year, end_year=end_year)
    # Save the fetched data to a JSON file
    await save_to_json(data, entity)


async def main():
    """
    Main function to run the application.
    It fetches data for a character, location, and episode, saves each to JSON files,
    and prints episode names that aired between 2017 and 2021.
    """
    async with RickAndMortyClient() as client:
        # Fetch and save data for Character, Location, and Episode
        await fetch_and_save(client, "character", )
        await fetch_and_save(client, "location", )
        await fetch_and_save(client, "episode", start_year=2017, end_year=2021)


# Entry point for the async application
if __name__ == "__main__":
    asyncio.run(main())
