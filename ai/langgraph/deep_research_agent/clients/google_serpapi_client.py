"""

"""


from pydantic.types import Json
import requests
import os

API_KEY = os.getenv('SERP_API_KEY')


class GoogleSearchService:
    
    def __init__(self) -> None:
        self.engine = 'google'
        self.url = "https://www.searchapi.io/api/v1/search"
        
    def search(self, query:str) -> Json:
        
        params = {
          "engine": self.engine,
          "q": query,
          "api_key": API_KEY
        }
        
        response = requests.get(self.url, params=params)
        
        return response.json