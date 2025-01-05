import os
import requests
from dotenv import load_dotenv

class OMDbAPI:
    API_URL = "http://www.omdbapi.com/"

    def __init__(self):
        """Initialize the OMDbAPI class, loading the API key from environment variables."""
        load_dotenv()
        self.API_KEY = os.getenv('API_KEY')
        if not self.API_KEY:
            raise Exception("Movie API Key not found in environment variables.")

    def fetch_movie_data(self, title):
        """Fetch movie data from OMDb API."""
        url = f'{self.API_URL}?apikey={self.API_KEY}&t={title}'
        response = requests.get(url)

        if response.status_code != 200:
            raise ConnectionError("Failed to connect to OMDb API")

        data = response.json()
        if data.get('Response') == 'False':
            raise ValueError("Movie not found")

        return {
            'title': data.get('Title'),
            'year': int(data.get('Year')),
            'rating': float(data.get('imdbRating')),
            'poster': data.get('Poster')
        }
