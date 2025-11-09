"""
Report Generation Node - Synthesizes search results into comprehensive reports.
"""

from typing import List

from langchain_core.messages import AIMessage, AnyMessage, HumanMessage
from configs.states import GraphOverallState
from constants.prompts.report_generation_node import LLM_SERVICE_USER_PROMPT
from clients.langchain_openai_client import LangChainOpenAILLMService


class ReportGenerationNode:
    """Node that generates comprehensive research reports from search results.

    This node takes all the search results gathered from multiple sources
    and uses an LLM to synthesize them into a well-structured, comprehensive
    research report.
    """

    def llm_response(self, messages: List[AnyMessage]) -> AIMessage:
        """Generate report using LLM based on search results.

        Args:
            messages: Conversation history including all search results

        Returns:
            AIMessage containing the generated research report
        """
        chat_model = LangChainOpenAILLMService(model_name="gpt-4o").get_model()

        # Create a copy to avoid modifying the original
        llm_messages = list(messages)
        llm_messages.append(HumanMessage(content=LLM_SERVICE_USER_PROMPT))

        response = chat_model.invoke(llm_messages)

        return response

    def __call__(self, state: GraphOverallState) -> GraphOverallState:
        """Execute report generation.

        Args:
            state: Current graph state containing search results

        Returns:
            Updated state with the generated report added to messages
        """
        messages = state["messages"]

        llm_response = self.llm_response(messages)

        return {"messages": [llm_response]}
