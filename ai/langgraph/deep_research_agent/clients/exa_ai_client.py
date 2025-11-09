"""
Exa AI search client for semantic web search.
"""

from exa_py import Exa
from exa_py.api import SearchResponse
import os
import logging

logger = logging.getLogger(__name__)

API_KEY = os.getenv("EXA_AI_API_KEY")

if not API_KEY:
    logger.warning("EXA_AI_API_KEY environment variable not set")


class ExaAISearchService:
    """Service for performing semantic searches using Exa AI.

    Requires EXA_AI_API_KEY environment variable to be set.
    """

    def __init__(self) -> None:
        """Initialize the Exa AI search service.

        Raises:
            ValueError: If EXA_AI_API_KEY is not set
        """
        if not API_KEY:
            raise ValueError("EXA_AI_API_KEY environment variable is required")
        self.client = Exa(api_key=API_KEY)

    def search(self, query: str, limit: int = 5) -> SearchResponse:
        """Execute an Exa AI search query.

        Args:
            query: Search query string
            limit: Maximum number of results to return

        Returns:
            SearchResponse object containing results

        Raises:
            Exception: If the search request fails
        """
        try:
            response = self.client.search(
                query=query,
                type="keyword",
                num_results=limit,
                contents={"text": {"maxCharacters": 1000}},
            )
            return response
        except Exception as e:
            logger.error(f"Exa AI search failed: {e}")
            raise
