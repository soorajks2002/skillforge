"""
State configurations for the deep research agent graph.

Defines the state schema used throughout the graph execution.
Uses LangGraph's MessagesState as the foundation.
"""

from langgraph.graph import MessagesState
from typing import Annotated
from langgraph.graph.message import add_messages


class GraphInputState(MessagesState):
    """Input state schema for the graph.

    Currently extends MessagesState with no additional fields.
    The graph expects an initial message from the user to start the research process.
    """

    pass


class GraphOutputState(MessagesState):
    """Output state schema for the graph.

    Currently extends MessagesState with no additional fields.
    The final output includes all messages in the conversation,
    with the last message being the generated research report.
    """

    pass


class GraphOverallState(MessagesState):
    """Overall state schema maintained throughout graph execution.

    This state is passed between all nodes in the graph.

    Inherited from MessagesState:
        messages: List of all messages in the conversation (HumanMessage, AIMessage, ToolMessage)
    """

    pass
