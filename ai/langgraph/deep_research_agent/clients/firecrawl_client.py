"""
Firecrawl client for web scraping and search.
"""

from firecrawl import Firecrawl
from firecrawl.types import SearchData
import os
import logging

logger = logging.getLogger(__name__)

API_KEY = os.getenv("FIRECRAWL_API_KEY")

if not API_KEY:
    logger.warning("FIRECRAWL_API_KEY environment variable not set")


class FirecrawlSearchService:
    """Service for performing web searches and scraping using Firecrawl.

    Requires FIRECRAWL_API_KEY environment variable to be set.
    """

    def __init__(self):
        """Initialize the Firecrawl search service.

        Raises:
            ValueError: If FIRECRAWL_API_KEY is not set
        """
        if not API_KEY:
            raise ValueError("FIRECRAWL_API_KEY environment variable is required")
        self.client = Firecrawl(api_key=API_KEY)

    def search(self, query: str, limit: int = 5) -> SearchData:
        """Execute a Firecrawl search query.

        Args:
            query: Search query string
            limit: Maximum number of results to return

        Returns:
            SearchData object containing web search results

        Raises:
            Exception: If the search request fails
        """
        try:
            response = self.client.search(query=query, limit=limit, sources=["web"])
            return response
        except Exception as e:
            logger.error(f"Firecrawl search failed: {e}")
            raise
