from typing import Literal
from langgraph.graph import StateGraph
from configs.states import GraphOverallState
from nodes.decision_maker_node import DecisionMakerNode
from nodes.human_interaction_node import HumanInteractionNode
from nodes.search_tool_node import SearchServiceNode
from nodes.report_generation_node import ReportGenerationNode
from langgraph.graph import START, END

builder = StateGraph(state_schema=GraphOverallState)

builder.add_node('decision_maker', DecisionMakerNode())
builder.add_node('human_interaction', HumanInteractionNode())
builder.add_node('search_services', SearchServiceNode())
builder.add_node('report_generation', ReportGenerationNode())

def route_from_decision_maker(state: GraphOverallState) -> Literal['human_interaction', 'search_services']:
    # Extract goto from Command in the last message
    return 'human_interaction'

builder.add_edge(START, 'decision_maker')
builder.add_conditional_edges('decision_maker', path=route_from_decision_maker, path_map=['human_interaction', 'search_services'])
builder.add_edge('human_interaction', 'decision_maker')
builder.add_edge('search_services', 'report_generation')
builder.add_edge('report_generation', END)

graph = builder.compile(
    checkpointer=None,
    interrupt_before=['human_interaction']
)

graph.get_graph().draw_mermaid_png(output_file_path='deep_research_agent_graph.png')