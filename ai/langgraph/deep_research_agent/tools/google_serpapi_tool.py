"""

"""


from firecrawl.v2.types import Dict
from pydantic.types import Json
from clients.google_serpapi_client import GoogleSearchService


TEMPLATE = """TITLE: {title}
TEXT SNIPPET: {snippet}

=========================

"""


class GoogleSearchTool:
    
    def __init__(self):
        self.service = GoogleSearchService()
    
    def post_process(self, search_data:Json) -> str:
        response = ""
        
        overview_content = search_data.get('ai_overview', {}).get('text_blocks', [])
        
        if overview_content:
            response = "GOOGLE AI OVERVIEW\n"
            
            for text_block in overview_content:
                response += text_block['snippet']
                
            response += "\n\n=============\n\n"
        
        web_search_data = search_data['organic_results']
        for index, entity in enumerate(web_search_data):
            response += f"RESULT: {index+1}\n"
            response += TEMPLATE.format(title=entity['title'], snippet=entity['snippet'])
            
        return response
    
    def get(self, query:str):
        
        search_data = self.service.search(query)
        
        response = self.post_process(search_data)
        
        return response