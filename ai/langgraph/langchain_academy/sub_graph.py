import dotenv
from langgraph.graph import StateGraph, START, END
from typing import Annotated, TypedDict
import operator

class OverallState(TypedDict):
    data: list[int]
    graph_one: list[int]
    graph_two: list[int]
    result: Annotated[list[int], operator.add]
    
class GraphOneState(TypedDict):
    graph_one: list[int]
    result: list[int]

class GraphTwoState(TypedDict):
    graph_two: list[int]
    result: list[int]
    

def graph_one_node_one(state: GraphOneState) -> GraphOneState:
    response = state["graph_one"]
    return {"graph_one": response}

def graph_one_node_two(state: GraphOneState) -> GraphOneState:
    # response = state["graph_one"].extend([0.1, 0.1, 0.1])
    return {"result": [0.1, 0.1, 0.1]}

graph_one = StateGraph(GraphOneState)
graph_one.add_node("graph_one_node_one", graph_one_node_one)
graph_one.add_node("graph_one_node_two", graph_one_node_two)
graph_one.add_edge(START, "graph_one_node_one")
graph_one.add_edge("graph_one_node_one", "graph_one_node_two")
graph_one.add_edge("graph_one_node_two", END)

graph_one_compiled = graph_one.compile()
    

def graph_two_node_one(state: GraphTwoState) -> GraphTwoState:
    response = state["graph_two"]
    return {"graph_two": response}

def graph_two_node_two(state: GraphTwoState) -> GraphTwoState:
    # response = state["result"].extend([0.2, 0.2, 0.2])
    return {"result": [0.2, 0.2, 0.2]}

graph_two = StateGraph(GraphTwoState)
graph_two.add_node("graph_two_node_one", graph_two_node_one)
graph_two.add_node("graph_two_node_two", graph_two_node_two)
graph_two.add_edge(START, "graph_two_node_one")
graph_two.add_edge("graph_two_node_one", "graph_two_node_two")
graph_two.add_edge("graph_two_node_two", END)

graph_two_compiled = graph_two.compile()


def main_graph_node_one(state: OverallState) -> OverallState:
    response = state["data"].extend([888])
    return {"data": response}

def main_graph_node_two(state: OverallState) -> OverallState:
    graph_one_data = [1,1]
    graph_two_data = [2,2]
    return {"graph_one": graph_one_data, "graph_two": graph_two_data}

main_graph = StateGraph(OverallState)

main_graph.add_node("main_graph_node_one", main_graph_node_one)
main_graph.add_node("main_graph_node_two", main_graph_node_two)
main_graph.add_node("graph_one_node", graph_one.compile())
main_graph.add_node("graph_two_node", graph_two.compile())

main_graph.add_edge(START, "main_graph_node_one")
main_graph.add_edge("main_graph_node_one", "main_graph_node_two")
main_graph.add_edge("main_graph_node_two", "graph_one_node")
main_graph.add_edge("main_graph_node_two", "graph_two_node")
main_graph.add_edge("graph_one_node", END)
main_graph.add_edge("graph_two_node", END)

main_graph_compiled = main_graph.compile()

main_graph_compiled.get_graph().draw_mermaid_png(output_file_path='mermaid_diagrams/sub_graph.png')


response = main_graph_compiled.invoke({"data": [0]})

print(response)