"""
Node to perform different searches.
"""


from typing import Dict, List, Any

from langchain_core.messages import AIMessage, ToolMessage
from tools.exa_ai_tool import ExaAISearchTool
from tools.firecrawl_tool import FireCrawlSearchTool
from tools.google_serpapi_tool import GoogleSearchTool
from tools.tavily_search_tool import TavilySearchTool
from configs.states import GraphOverallState


class SearchServiceNode:
    
    def get_all_search_results(self, query:str) -> Dict:
        response = dict()
        
        response['exai'] = ExaAISearchTool().get(query)
        response['firecrawl'] = FireCrawlSearchTool().get(query)
        response['google_search'] = GoogleSearchTool().get(query)
        response['tavily'] = TavilySearchTool().get(query)
        
        return response
        
    def post_process(self, search_results:Dict) -> List[ToolMessage]:
        
        response = []
        
        response.append(ToolMessage(contet=f"The following is the search result for exai tool\n {response['exai']}"))
        response.append(ToolMessage(contet=f"The following is the search result for firecrawl tool\n {response['firecrawl']}"))
        response.append(ToolMessage(contet=f"The following is the search result for google search tool\n {response['google_search']}"))
        response.append(ToolMessage(contet=f"The following is the search result for tavily tool\n {response['tavily']}"))
        
        return response
        
    
    def __call__(self, state:GraphOverallState) -> Any:
        
        last_message: AIMessage = state['messages'][-1]
        query = last_message.tool_calls[0]['args']['query']
        
        search_results = self.get_all_search_results(query)
        
        messages = self.post_process(search_results)
        
        return {'messages': messages}