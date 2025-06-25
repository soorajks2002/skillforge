from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from operator import add

def custom_reducer(left: list|None, right: list|None) -> list:
    """
    Custom reducer for the state graph.
    """
    
    if left is None:
        left = []
    if right is None:
        right = []

    return left + right


class CustomState(TypedDict):
    value: Annotated[list[int], custom_reducer]
    
class State(TypedDict):
    value: Annotated[list[int], add]
    
    
def custom_node_1(state: CustomState) -> CustomState:
    return {"value": [10]}

def custom_node_2(state: CustomState) -> CustomState:
    return {"value": [20]}

def custom_node_3(state: CustomState) -> CustomState:
    return {"value": [30]}

def custom_node_4(state: CustomState) -> CustomState:
    return {"value": [40]}


custom_builder = StateGraph(CustomState)
custom_builder.add_node("node_1", custom_node_1)
custom_builder.add_node("node_2", custom_node_2)
custom_builder.add_node("node_3", custom_node_3)
custom_builder.add_node("node_4", custom_node_4)

custom_builder.add_edge(START, "node_1")
custom_builder.add_edge("node_1", "node_2")
custom_builder.add_edge("node_2", "node_3")
custom_builder.add_edge("node_2", "node_4")
custom_builder.add_edge("node_3", END)
custom_builder.add_edge("node_4", END)

custom_graph = custom_builder.compile()

response_custom = custom_graph.invoke({"value": []})
print(response_custom)

print("-"*40)
response_custom = custom_graph.invoke({"value": [0]})
print(response_custom)

print("-"*40)
response_custom = custom_graph.invoke({"value": None})
print(response_custom)

print("-"*40)


def simple_node_1(state: State) -> State:
    return {"value": [10]}

def simple_node_2(state: State) -> State:
    return {"value": [20]}

def simple_node_3(state: State) -> State:
    return {"value": [30]}

def simple_node_4(state: State) -> State:
    return {"value": [40]}


simple_builder = StateGraph(State)
simple_builder.add_node("node_1", simple_node_1)
simple_builder.add_node("node_2", simple_node_2)
simple_builder.add_node("node_3", simple_node_3)
simple_builder.add_node("node_4", simple_node_4)

simple_builder.add_edge(START, "node_1")
simple_builder.add_edge("node_1", "node_2")
simple_builder.add_edge("node_2", "node_3")
simple_builder.add_edge("node_2", "node_4")
simple_builder.add_edge("node_3", END)
simple_builder.add_edge("node_4", END)

simple_graph = simple_builder.compile()

response_simple = simple_graph.invoke({"value": []})
print(response_simple)

print("-"*40)
response_simple = simple_graph.invoke({"value": [0]})
print(response_simple)

print("-"*40)
try:
    response_simple = simple_graph.invoke({"value": None})
    print(response_simple)
except Exception as e:
    print(e)