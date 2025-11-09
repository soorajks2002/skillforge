"""
Node to perform different searches across multiple search services.
Supports both synchronous and asynchronous execution.
"""

from typing import Dict, List
import logging
import asyncio
from concurrent.futures import ThreadPoolExecutor

from langchain_core.messages import AIMessage, ToolMessage
from tools.exa_ai_tool import ExaAISearchTool
from tools.firecrawl_tool import FireCrawlSearchTool
from tools.google_serpapi_tool import GoogleSearchTool
from tools.tavily_search_tool import TavilySearchTool
from configs.states import GraphOverallState

logger = logging.getLogger(__name__)


class SearchServiceNode:
    """Node that executes searches across multiple search engines.

    This node aggregates results from four different search services:
    - Exa AI: Semantic search
    - Firecrawl: Web scraping and search
    - Google SerpAPI: Traditional web search
    - Tavily: AI-powered research

    Searches can be executed in parallel for better performance.
    """

    def __init__(self, use_async: bool = False):
        """Initialize the search service node.

        Args:
            use_async: If True, executes searches in parallel using ThreadPoolExecutor
        """
        self.use_async = use_async

    def _execute_single_search(
        self, service_name: str, tool_class, query: str
    ) -> tuple[str, str]:
        """Execute a single search and return results with error handling.

        Args:
            service_name: Name of the search service
            tool_class: Search tool class to instantiate
            query: Search query string

        Returns:
            Tuple of (service_name, result_string)
        """
        try:
            result = tool_class().get(query)
            return (service_name, result)
        except Exception as e:
            logger.error(f"{service_name} search failed: {e}")
            return (service_name, f"Error: {str(e)}")

    def get_all_search_results_parallel(self, query: str) -> Dict[str, str]:
        """Execute searches in parallel using ThreadPoolExecutor.

        Args:
            query: Search query string

        Returns:
            Dictionary mapping service names to their search results
        """
        search_configs = [
            ("exai", ExaAISearchTool),
            ("firecrawl", FireCrawlSearchTool),
            ("google_search", GoogleSearchTool),
            ("tavily", TavilySearchTool),
        ]

        results = {}

        with ThreadPoolExecutor(max_workers=4) as executor:
            futures = [
                executor.submit(self._execute_single_search, name, tool_class, query)
                for name, tool_class in search_configs
            ]

            for future in futures:
                service_name, result = future.result()
                results[service_name] = result

        return results

    def get_all_search_results(self, query: str) -> Dict[str, str]:
        """Execute search across all available search services.

        Args:
            query: Search query string

        Returns:
            Dictionary mapping service names to their search results
        """
        if self.use_async:
            return self.get_all_search_results_parallel(query)

        response = {}

        # Execute searches sequentially with individual error handling
        try:
            response["exai"] = ExaAISearchTool().get(query)
        except Exception as e:
            logger.error(f"Exa AI search failed: {e}")
            response["exai"] = f"Error: {str(e)}"

        try:
            response["firecrawl"] = FireCrawlSearchTool().get(query)
        except Exception as e:
            logger.error(f"Firecrawl search failed: {e}")
            response["firecrawl"] = f"Error: {str(e)}"

        try:
            response["google_search"] = GoogleSearchTool().get(query)
        except Exception as e:
            logger.error(f"Google search failed: {e}")
            response["google_search"] = f"Error: {str(e)}"

        try:
            response["tavily"] = TavilySearchTool().get(query)
        except Exception as e:
            logger.error(f"Tavily search failed: {e}")
            response["tavily"] = f"Error: {str(e)}"

        return response

    def post_process(
        self, search_results: Dict, tool_call_id: str
    ) -> List[ToolMessage]:
        """Convert search results into ToolMessages.

        Args:
            search_results: Dictionary containing results from all search services
            tool_call_id: ID of the tool call that initiated the search

        Returns:
            List of ToolMessage objects with formatted search results
        """
        messages = []

        for tool_name, result in search_results.items():
            messages.append(
                ToolMessage(
                    content=f"Search results from {tool_name}:\n\n{result}",
                    tool_call_id=tool_call_id,
                    name=f"{tool_name}_search",
                )
            )

        return messages

    def __call__(self, state: GraphOverallState) -> Dict:
        """Execute search across all services and return results.

        Args:
            state: Current graph state containing messages

        Returns:
            Dictionary with messages key containing search results
        """
        last_message: AIMessage = state["messages"][-1]
        tool_call = last_message.tool_calls[0]
        query = tool_call["args"]["query"]
        tool_call_id = tool_call["id"]

        search_results = self.get_all_search_results(query)

        messages = self.post_process(search_results, tool_call_id)

        return {"messages": messages}
