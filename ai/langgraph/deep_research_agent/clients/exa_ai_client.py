"""

"""


from exa_py import Exa
from exa_py.api import SearchResponse
import os

API_KEY = os.getenv('EXA_AI_API_KEY')


class ExaAISearchService:
    
    def __init__(self) -> None:
        self.client = Exa(
            api_key=API_KEY
        )
        
    def search(self, query:str, limit:int=5)->SearchResponse:
        response = self.client.search(
            query=query,
            type='keyword',
            num_results=limit,
            contents={"text": {"maxCharacters": 1000}}
        )
        
        return response