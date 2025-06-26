from langgraph.graph import StateGraph, START, END
from langgraph.constants import Send
from pydantic import BaseModel
from typing import Annotated
import operator
from langgraph.checkpoint.memory import MemorySaver


class CustomState(BaseModel):
    data: list[int]
    result: Annotated[list[int], operator.add]
    sum: int | None = None
    
class MultiplicationState(BaseModel):
    data: int
    multiplier: int
    

def simulate_input_node(state: CustomState):
    return {"data": [1,2,3,4,5]}


def multiplication_node(state: MultiplicationState):
    return {"result": [state.data * state.multiplier]}

def sum_node(state: CustomState):
    print(f"\n--\n{state}\n--\n")
    return {"sum": sum(state.result)}


def call_multiple_nodes_in_parallel(state: CustomState):
    response = [Send('multiplication_node', MultiplicationState(data=val, multiplier=2)) for val in state.data]
    print(f"\n--\n{response}\n--\n")
    return response


builder = StateGraph(CustomState)

builder.add_node("simulate_input_node", simulate_input_node)
builder.add_node("multiplication_node", multiplication_node)
builder.add_node("sum_node", sum_node)

builder.add_edge(START, "simulate_input_node")
builder.add_conditional_edges('simulate_input_node', call_multiple_nodes_in_parallel, ['multiplication_node'])
builder.add_edge('multiplication_node', 'sum_node')
builder.add_edge('sum_node', END)

memory_saver = MemorySaver()
graph = builder.compile(checkpointer=memory_saver)

graph.get_graph().draw_mermaid_png(output_file_path='mermaid_diagrams/map_reduce_graph.png')


thread = {'configurable': {'thread_id': '1'}}
response = graph.invoke({'data':[]}, config=thread)

print(response)


print("---\n---\n---\n\n")

state_history = graph.get_state_history(config=thread)
states = [state for state in state_history]

for state in states:
    print(state)
    print("\n--\n")