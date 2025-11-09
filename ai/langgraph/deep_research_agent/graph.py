from typing import Literal
from langgraph.graph import StateGraph
from configs.states import GraphOverallState
from nodes.decision_maker_node import DecisionMakerNode
from nodes.human_interaction_node import HumanInteractionNode
from nodes.search_tool_node import SearchServiceNode
from nodes.report_generation_node import ReportGenerationNode
from langgraph.graph import START, END

# Initialize the state graph
builder = StateGraph(state_schema=GraphOverallState)

# Add nodes with parallel search enabled for better performance
builder.add_node("decision_maker", DecisionMakerNode())
builder.add_node("human_interaction", HumanInteractionNode())
builder.add_node(
    "search_services", SearchServiceNode(use_async=True)
)  # Enable parallel searches
builder.add_node("report_generation", ReportGenerationNode())


def route_from_decision_maker(
    state: GraphOverallState,
) -> Literal["human_interaction", "search_services"]:
    """Route based on the last message from decision maker.

    If the last message contains tool_calls, route to search_services.
    Otherwise, route to human_interaction for clarification.
    """
    last_message = state["messages"][-1]
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "search_services"
    return "human_interaction"


# Define graph edges
builder.add_edge(START, "decision_maker")
builder.add_conditional_edges(
    "decision_maker",
    path=route_from_decision_maker,
    path_map=["human_interaction", "search_services"],
)
builder.add_edge("human_interaction", "decision_maker")
builder.add_edge("search_services", "report_generation")
builder.add_edge("report_generation", END)

# Compile the graph with human-in-the-loop interrupt
graph = builder.compile(checkpointer=None, interrupt_before=["human_interaction"])

# Generate visualization
graph.get_graph().draw_mermaid_png(output_file_path="deep_research_agent_graph.png")
