"""
Tavily AI search client for comprehensive web research.
"""

from typing import Dict
from tavily import TavilyClient
import os
import logging

logger = logging.getLogger(__name__)

API_KEY = os.getenv("TAVILY_API_KEY")

if not API_KEY:
    logger.warning("TAVILY_API_KEY environment variable not set")


class TavilySearchService:
    """Service for performing AI-powered searches using Tavily.

    Requires TAVILY_API_KEY environment variable to be set.
    """

    def __init__(self):
        """Initialize the Tavily search service.

        Raises:
            ValueError: If TAVILY_API_KEY is not set
        """
        if not API_KEY:
            raise ValueError("TAVILY_API_KEY environment variable is required")
        self.client = TavilyClient(api_key=API_KEY)

    def search(self, query: str, limit: int = 5) -> Dict:
        """Execute a Tavily search query.

        Args:
            query: Search query string
            limit: Maximum number of results to return

        Returns:
            Dictionary containing search results

        Raises:
            Exception: If the search request fails
        """
        try:
            response = self.client.search(
                query=query,
                max_results=limit,
                search_depth="basic",
                include_answer=False,
            )
            return response
        except Exception as e:
            logger.error(f"Tavily search failed: {e}")
            raise
