"""
Google SerpAPI client for web search functionality.
"""

from typing import Dict
import requests
import os
import logging

logger = logging.getLogger(__name__)

API_KEY = os.getenv("SERP_API_KEY")

if not API_KEY:
    logger.warning("SERP_API_KEY environment variable not set")


class GoogleSearchService:
    """Service for performing Google searches via SearchAPI.io.

    Requires SERP_API_KEY environment variable to be set.
    """

    def __init__(self) -> None:
        """Initialize the Google search service."""
        if not API_KEY:
            raise ValueError("SERP_API_KEY environment variable is required")
        self.engine = "google"
        self.url = "https://www.searchapi.io/api/v1/search"

    def search(self, query: str, max_retries: int = 3) -> Dict:
        """Execute a Google search query.

        Args:
            query: Search query string
            max_retries: Maximum number of retry attempts

        Returns:
            Dictionary containing search results

        Raises:
            ValueError: If API key is not set
            requests.RequestException: If the API request fails after retries
        """
        params = {"engine": self.engine, "q": query, "api_key": API_KEY}

        for attempt in range(max_retries):
            try:
                response = requests.get(self.url, params=params, timeout=30)
                response.raise_for_status()
                return response.json()
            except requests.RequestException as e:
                logger.error(f"Google search attempt {attempt + 1} failed: {e}")
                if attempt == max_retries - 1:
                    raise

        return {}
