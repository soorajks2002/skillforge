"""

"""


from typing import Dict
from tavily import TavilyClient
import os


API_KEY = os.getenv('TAVILY_API_KEY')


class TavilySearchService:

    def __init__(self):
        self.client = TavilyClient(
            api_key=API_KEY
        )

    def search(self, query:str, limit:int=5) -> Dict:
        response = self.client.search(
            query=query,
            max_results=limit,
            search_depth='basic',
            include_answer=False
        )

        return response
