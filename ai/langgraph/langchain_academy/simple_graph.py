from pydantic import BaseModel
import random
from typing import Literal
from langgraph.graph import StateGraph, START, END


class State(BaseModel):
    graph_state: str


def node_1(state: State):
    print("--- Node 1 Executed ---")
    return {"graph_state": state.graph_state + " -Node 1- "}


def node_2(state: State):
    print("--- Node 2 Executed ---")
    return {"graph_state": state.graph_state + " -Node 2- "}


def node_3(state: State):
    print("--- Node 3 Executed ---")
    return {"graph_state": state.graph_state + " -Node 3- "}


def node_4(state: State):
    print("--- Node 4 Executed ---")
    return {"graph_state": state.graph_state + " -Node 4- "}


def conditional_edge(state) -> Literal["node_3", "node_4"]:
    # conditional edge are implemented as functions that return the name of the next node
    # Output type is needed to get proper mermaid graph

    data = state.graph_state

    if random.random() < 0.5:
        return "node_3"
    else:
        return "node_4"


graph = StateGraph(State)
graph.add_node("node_1", node_1)
graph.add_node("node_2", node_2)
graph.add_node("node_3", node_3)
graph.add_node("node_4", node_4)


graph.add_edge(START, "node_1")
graph.add_edge("node_1", "node_2")
graph.add_conditional_edges("node_2", conditional_edge)
graph.add_edge("node_3", END)
graph.add_edge("node_4", END)


compiled_graph = graph.compile()


# compiled_graph.get_graph().draw_mermaid_png(output_file_path="graphs/simple_graph.png")


input_data = {
    "graph_state": " -- State data -- "
}

response = compiled_graph.invoke(input_data)

print(response)