"""
Google Search Tool - Wrapper for Google SerpAPI search service.
"""

from typing import Dict
from clients.google_serpapi_client import GoogleSearchService


TEMPLATE = """TITLE: {title}
TEXT SNIPPET: {snippet}

=========================

"""


class GoogleSearchTool:
    """Tool for executing Google searches and formatting results.

    Uses SearchAPI.io to access Google search results including AI overviews.
    """

    def __init__(self):
        """Initialize the Google search tool."""
        self.service = GoogleSearchService()

    def post_process(self, search_data: Dict) -> str:
        """Format Google search results into a readable string.

        Args:
            search_data: Raw search response from Google SerpAPI

        Returns:
            Formatted string with search results including AI overview if available
        """
        response = ""

        # Add AI Overview if available
        overview_content = search_data.get("ai_overview", {}).get("text_blocks", [])

        if overview_content:
            response = "GOOGLE AI OVERVIEW\n"

            for text_block in overview_content:
                response += text_block.get("snippet", "")

            response += "\n\n=============\n\n"

        # Add organic search results
        web_search_data = search_data.get("organic_results", [])
        for index, entity in enumerate(web_search_data):
            response += f"RESULT: {index + 1}\n"
            response += TEMPLATE.format(
                title=entity.get("title", "N/A"), snippet=entity.get("snippet", "N/A")
            )

        return response

    def get(self, query: str) -> str:
        """Execute a Google search and return formatted results.

        Args:
            query: Search query string

        Returns:
            Formatted search results as a string
        """
        search_data = self.service.search(query)
        response = self.post_process(search_data)
        return response
