"""

"""


from typing import Dict
from clients.tavily_client import TavilySearchService


TEMPLATE = """TITLE: {title}
CONTENT: {content}

=========================

"""


class TavilySearchTool:
    
    def __init__(self):
        self.service = TavilySearchService()
    
    def post_process(self, search_data:Dict) -> str:
        response = ""
        
        web_search_data = search_data['results']
        for index, entity in enumerate(web_search_data):
            response += f"RESULT: {index+1}\n"
            response += TEMPLATE.format(title=entity['title'], content=entity['content'])
            
        return response
    
    def get(self, query:str) -> str:
        
        search_data = self.service.search(query)
        
        response = self.post_process(search_data)
        
        return response