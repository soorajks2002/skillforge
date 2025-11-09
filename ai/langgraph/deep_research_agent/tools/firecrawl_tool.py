"""
Firecrawl Search Tool - Wrapper for Firecrawl web scraping and search service.
"""

from clients.firecrawl_client import FirecrawlSearchService
from firecrawl.types import SearchData


TEMPLATE = """URL: {url}
TITLE: {title}
DESCRIPTION: {description}

=========================

"""


class FireCrawlSearchTool:
    """Tool for executing Firecrawl searches and formatting results.

    Firecrawl provides web scraping and search capabilities.
    """

    def __init__(self):
        """Initialize the Firecrawl search tool."""
        self.service = FirecrawlSearchService()

    def post_process(self, search_data: SearchData) -> str:
        """Format Firecrawl search results into a readable string.

        Args:
            search_data: SearchData object from Firecrawl API

        Returns:
            Formatted string with search results
        """
        response = ""

        web_search_data = search_data.web if hasattr(search_data, "web") else []
        for index, entity in enumerate(web_search_data):
            response += f"RESULT: {index + 1}\n"
            response += TEMPLATE.format(
                url=getattr(entity, "url", "N/A"),
                title=getattr(entity, "title", "N/A"),
                description=getattr(entity, "description", "N/A"),
            )

        return response

    def get(self, query: str) -> str:
        """Execute a Firecrawl search and return formatted results.

        Args:
            query: Search query string

        Returns:
            Formatted search results as a string
        """
        search_data = self.service.search(query)
        response = self.post_process(search_data)
        return response
