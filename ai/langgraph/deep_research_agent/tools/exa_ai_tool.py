"""

"""


from clients.exa_ai_client import ExaAISearchService
from exa_py.api import SearchResponse


TEMPLATE = """URL: {url}
TITLE: {title}
SUMMARY: {description}

=========================

"""


class ExaAISearchTool:
    
    def __init__(self):
        self.service = ExaAISearchService()
    
    def post_process(self, search_data:SearchResponse) -> str:
        response = ""
        
        web_search_data = search_data.results
        
        for index, entity in enumerate(web_search_data):
            response += f"RESULT: {index+1}\n"
            response += TEMPLATE.format(url=entity['url'], title=entity['title'], description=entity['summary'])
            
        return response
    
    def get(self, query:str):
        
        search_data = self.service.search(query)
        
        response = self.post_process(search_data)
        
        return response