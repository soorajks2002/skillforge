"""
Exa AI Search Tool - Wrapper for Exa AI semantic search service.
"""

from clients.exa_ai_client import ExaAISearchService
from exa_py.api import SearchResponse


TEMPLATE = """URL: {url}
TITLE: {title}
SUMMARY: {description}

=========================

"""


class ExaAISearchTool:
    """Tool for executing Exa AI semantic searches and formatting results.

    Exa AI provides semantic search capabilities for more contextual results.
    """

    def __init__(self):
        """Initialize the Exa AI search tool."""
        self.service = ExaAISearchService()

    def post_process(self, search_data: SearchResponse) -> str:
        """Format Exa AI search results into a readable string.

        Args:
            search_data: SearchResponse object from Exa AI API

        Returns:
            Formatted string with search results
        """
        response = ""

        web_search_data = search_data.results

        for index, entity in enumerate(web_search_data):
            response += f"RESULT: {index + 1}\n"
            response += TEMPLATE.format(
                url=entity.get("url", "N/A"),
                title=entity.get("title", "N/A"),
                description=entity.get("summary", "N/A"),
            )

        return response

    def get(self, query: str) -> str:
        """Execute an Exa AI search and return formatted results.

        Args:
            query: Search query string

        Returns:
            Formatted search results as a string
        """
        search_data = self.service.search(query)
        response = self.post_process(search_data)
        return response
