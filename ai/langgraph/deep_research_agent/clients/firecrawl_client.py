"""

"""


from firecrawl import Firecrawl
from firecrawl.types import SearchData
import os


API_KEY = os.getenv('FIRECRAWL_API_KEY')


class FirecrawlSearchService:
    
    def __init__(self):
        self.client = Firecrawl(
            api_key=API_KEY
        )
        
    def search(self, query:str, limit:int=5) -> SearchData:
        response = self.client.search(
            query=query,
            limit=limit,
            sources=['web']
        )
        
        return response