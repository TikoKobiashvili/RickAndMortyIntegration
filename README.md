
# Rick and Morty API Integration

This project provides an asynchronous Python client for interacting with the [Rick and Morty API](https://rickandmortyapi.com/), which allows fetching data on characters, locations, and episodes. The app also saves this data in JSON format and filters episodes by date range.

## Features

- **Asynchronous Client**: Utilizes `httpx` for making asynchronous HTTP requests.
- **Data Fetching**: Retrieves all data for characters, locations, and episodes from the Rick and Morty API.
- **JSON Output**: Saves retrieved data to JSON files, including a unique ID and the raw API response.
- **Episode Filtering**: Prints episode names that aired within a specified date range.

## Technologies

- Python 3.8+
- `httpx` for asynchronous HTTP requests
- `pytest` and `pytest-asyncio` for testing
- `pytest-httpx` for mocking HTTP requests in tests

## Setup

### 1. Clone the repository
```bash
git clone https://github.com/TikoKobiashvili/RickAndMortyIntegration.git
cd RickAndMortyIntegration
```


### 2. Install Dependencies

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Running the Application

```bash
python -m app.main
```

## Application Structure

- `rick_and_morty_client.py`: Contains the RickAndMortyClient class that handles async API calls to fetch characters, locations, and episodes data.
- `main.py`: The main script that orchestrates data fetching, saving, and filtering based on date range.

### Example Output

After running the app, you should find three JSON files in the working directory:

**character.json**
**location.json**
**episode.json**
{
    "id": "<unique_id>",
    "RawData": [<API response data>]
}

## Testing

### Run Tests

To run the tests, use:
```bash
pytest
```

## Acknowledgements

- `Rick and Morty API` for providing a comprehensive public API.
- `httpx` for async HTTP support in Python.
