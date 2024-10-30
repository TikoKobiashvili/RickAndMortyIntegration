# rick_and_morty_client.py
import httpx

# Base URL for the Rick and Morty API
BASE_URL = "https://rickandmortyapi.com/api"


class RickAndMortyClient:
    """
    Asynchronous client for fetching data from the Rick and Morty API.
    This client uses httpx to perform async HTTP GET requests to fetch
    information on characters, locations, and episodes.
    """

    def __init__(self):
        # Initialize the HTTPX AsyncClient
        self.client = httpx.AsyncClient()

    async def __aenter__(self):
        # Enter the async context manager and open the HTTP client session
        await self.client.__aenter__()
        return self

    async def __aexit__(self, *args):
        # Close the HTTP client session when exiting the context manager
        await self.client.__aexit__(*args)

    async def fetch_data(self, url):
        """
        Fetch data from a specified url.
        Parameters:
            url (str): The specific URL to fetch data from.
        Returns:
            dict: JSON response from the API as a Python dictionary.
        """
        response = await self.client.get(url)
        response.raise_for_status()  # Raise error if the response is not successful

        return response.json()

    async def fetch_all_data(self, endpoint):
        """
        Fetch data from a specified endpoint.
        Parameters:
            endpoint (str): The specific API endpoint to fetch data from. (character,episode,location)
        Returns:
            list: list of  dictionaries.
        """
        url = f"{BASE_URL}/{endpoint}"

        response = await self.fetch_data(url)
        result = response.get('results')
        # To go through all pages, if there are any
        next_page = response.get('info').get('next')
        while next_page:
            response = await self.fetch_data(next_page)
            result.extend(response.get('results'))
            next_page = response.get('info').get('next')

        return result

