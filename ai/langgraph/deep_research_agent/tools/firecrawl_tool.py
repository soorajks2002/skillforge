"""

"""


from clients.firecrawl_client import FirecrawlSearchService
from firecrawl.types import SearchData


TEMPLATE = """URL: {url}
TITLE: {title}
DESCRIPTION: {description}

=========================

"""


class FireCrawlSearchTool:
    
    def __init__(self):
        self.service = FirecrawlSearchService()
    
    def post_process(self, search_data:SearchData) -> str:
        response = ""
        
        web_search_data = search_data.web
        for index, entity in enumerate(web_search_data):
            response += f"RESULT: {index+1}\n"
            response += TEMPLATE.format(url=entity.url, title=entity.title, description=entity.description)
            
        return response
    
    def get(self, query:str):
        
        search_data = self.service.search(query)
        
        response = self.post_process(search_data)
        
        return response