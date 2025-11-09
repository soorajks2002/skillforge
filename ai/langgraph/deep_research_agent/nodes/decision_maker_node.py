"""
Main Node for the agent.
Decides and finalizes the plan for any new question.
"""

from typing import Any, Dict, List, Tuple
from langchain_core.messages import AIMessage, AnyMessage, SystemMessage, ToolMessage
from langchain_core.messages.tool import ToolCall
from langgraph.graph.state import Command
from configs.states import GraphOverallState
from constants.prompts.decision_maker_node import (
    LLM_SERVICE_SYSTEM_PROMPT,
    llm_service_output_format,
)
from clients.langchain_openai_client import LangChainOpenAILLMService
from langgraph.graph.message import add_messages
import uuid


class DecisionMakerNode:
    """Decision maker node that determines the next action in the research flow.

    This node analyzes user queries and decides whether to:
    1. Ask for clarification (human-in-the-loop)
    2. Start the search process with available information
    """

    def pre_process(self, messages: List[AnyMessage]) -> List[AnyMessage]:
        """Filter out tool messages from the message history.

        Args:
            messages: List of all messages in the conversation

        Returns:
            List of messages excluding ToolMessages
        """
        non_tool_messages = []

        for message in messages:
            if isinstance(message, ToolMessage):
                continue

            non_tool_messages.append(message)

        return non_tool_messages

    def llm_response(self, messages: List[AnyMessage]) -> Dict:
        """Get structured response from LLM about next steps.

        Args:
            messages: Preprocessed message history

        Returns:
            Structured output containing next_step and relevant questions
        """
        llm_messages: List[AnyMessage] = [SystemMessage(LLM_SERVICE_SYSTEM_PROMPT)]
        llm_messages.extend(messages)

        chat_model = LangChainOpenAILLMService(model_name="gpt-5-nano").get_model()
        chat_model = chat_model.with_structured_output(llm_service_output_format)

        response = chat_model.invoke(llm_messages)

        return response

    def post_process(
        self, response: llm_service_output_format
    ) -> Tuple[str, AIMessage]:
        """Convert LLM response into appropriate message and routing decision.

        Args:
            response: Structured output from LLM

        Returns:
            Tuple of (next_node_name, message_to_add)
        """
        next_step = response.next_step

        if next_step == "deep_dive":
            deep_dive_question = response.deep_dive_question
            tool_message = AIMessage(content=deep_dive_question)

            return "human_interaction", tool_message

        start_search_question = response.start_search_question
        tool_message = AIMessage(
            content=f"Starting deep research on: {start_search_question}",
            tool_calls=[
                {
                    "name": "combined_search_tool",
                    "args": {"query": start_search_question},
                    "id": str(uuid.uuid4()),
                }
            ],
        )

        return "search_services", tool_message

    def __call__(self, state: GraphOverallState) -> Command:
        """Execute the decision making process.

        Args:
            state: Current graph state

        Returns:
            Command object directing to next node with updated state
        """
        messages = state["messages"]

        cleaned_messages = self.pre_process(messages)

        llm_response = self.llm_response(cleaned_messages)

        next_node, tool_message = self.post_process(llm_response)

        # Update messages properly
        updated_messages = list(state["messages"])
        updated_messages.append(tool_message)

        updated_state = {**state, "messages": updated_messages}

        return Command(goto=next_node, update=updated_state)
