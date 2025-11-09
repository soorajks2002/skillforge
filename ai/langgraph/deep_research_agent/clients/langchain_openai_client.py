"""
LangChain OpenAI client for LLM interactions.
"""

from langchain_openai import ChatOpenAI
import os
import logging

logger = logging.getLogger(__name__)

API_KEY = os.getenv("OPENAI_API_KEY")

if not API_KEY:
    logger.warning("OPENAI_API_KEY environment variable not set")


class LangChainOpenAILLMService:
    """Service for interacting with OpenAI models via LangChain.

    Requires OPENAI_API_KEY environment variable to be set.
    """

    def __init__(self, model_name: str, use_responses_api: bool = True):
        """Initialize the OpenAI LLM service.

        Args:
            model_name: Name of the OpenAI model to use (e.g., 'gpt-4o-mini', 'gpt-4o')
            use_responses_api: Whether to use the responses API format

        Raises:
            ValueError: If OPENAI_API_KEY is not set
        """
        if not API_KEY:
            raise ValueError("OPENAI_API_KEY environment variable is required")
        self.model_name = model_name
        self.use_responses_api = use_responses_api

    def get_model(self) -> ChatOpenAI:
        """Get configured ChatOpenAI model instance.

        Returns:
            Configured ChatOpenAI model
        """
        return ChatOpenAI(
            model=self.model_name,
            temperature=0.6,
            max_completion_tokens=20000,
            use_responses_api=self.use_responses_api,
            api_key=API_KEY,
        )
