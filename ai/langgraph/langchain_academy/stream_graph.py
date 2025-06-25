from langgraph.graph import StateGraph, START, END
from typing import TypedDict, List, Annotated
from operator import add

class CustomState(TypedDict):
    data: Annotated[List[int], add]
    
    
def node_1(state: CustomState) -> CustomState:
    return CustomState(data=[1])

def node_2(state: CustomState) -> CustomState:
    return CustomState(data=[2])

def node_3(state: CustomState) -> CustomState:
    return CustomState(data=[3])

def node_4(state: CustomState) -> CustomState:
    return CustomState(data=[4])

def node_5(state: CustomState) -> CustomState:
    return CustomState(data=[5])


builder = StateGraph(CustomState)

builder.add_node('node_1', node_1)
builder.add_node('node_2', node_2)
builder.add_node('node_3', node_3)
builder.add_node('node_4', node_4)
builder.add_node('node_5', node_5)

builder.add_edge(START, 'node_1')
builder.add_edge('node_1', 'node_2')
builder.add_edge('node_2', 'node_3')
builder.add_edge('node_3', 'node_4')
builder.add_edge('node_4', 'node_5')
builder.add_edge('node_5', END)

graph = builder.compile()

graph.get_graph(xray=True).draw_mermaid_png(output_file_path="mermaid_diagrams/stream_graph.png")

# There are two types of stream:
# 1. Stream updates made by each node
# 2. Stream entire state after each node

print("Stream updates made by each node")

for chunk in graph.stream(CustomState(data=[]), stream_mode='updates'):
    print(chunk)
    
    
print("Stream entire state after each node")

for chunk in graph.stream(CustomState(data=[]), stream_mode='values'):
    print(chunk)