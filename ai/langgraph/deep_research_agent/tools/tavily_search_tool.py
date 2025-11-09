"""
Tavily Search Tool - Wrapper for Tavily AI search service.
"""

from typing import Dict
from clients.tavily_client import TavilySearchService


TEMPLATE = """TITLE: {title}
CONTENT: {content}

=========================

"""


class TavilySearchTool:
    """Tool for executing Tavily AI searches and formatting results.

    Tavily provides AI-powered search with comprehensive content extraction.
    """

    def __init__(self):
        """Initialize the Tavily search tool."""
        self.service = TavilySearchService()

    def post_process(self, search_data: Dict) -> str:
        """Format Tavily search results into a readable string.

        Args:
            search_data: Raw search response from Tavily API

        Returns:
            Formatted string with search results
        """
        response = ""

        web_search_data = search_data.get("results", [])
        for index, entity in enumerate(web_search_data):
            response += f"RESULT: {index + 1}\n"
            response += TEMPLATE.format(
                title=entity.get("title", "N/A"), content=entity.get("content", "N/A")
            )

        return response

    def get(self, query: str) -> str:
        """Execute a Tavily search and return formatted results.

        Args:
            query: Search query string

        Returns:
            Formatted search results as a string
        """
        search_data = self.service.search(query)
        response = self.post_process(search_data)
        return response
