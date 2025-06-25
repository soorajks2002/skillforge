from langgraph.graph import StateGraph, START, END
from typing import TypedDict, List, Annotated
from operator import add
from langgraph.checkpoint.memory import MemorySaver

class CustomState(TypedDict):
    data: Annotated[List[int], add]
    
    
def node_1(state: CustomState) -> CustomState:
    return CustomState(data=[1])


def node_2(state: CustomState) -> CustomState:
    return CustomState(data=[2])


builder = StateGraph(CustomState)

builder.add_node('node_1', node_1)
builder.add_node('node_2', node_2)

builder.add_edge(START, 'node_1')
builder.add_edge('node_1', 'node_2')
builder.add_edge('node_2', END)

memory_saver = MemorySaver()

graph = builder.compile(interrupt_before=['node_2'], checkpointer=memory_saver)

thread = {
    'configurable': {
        'thread_id': '123'
    }
}

response = graph.invoke(CustomState(data=[]), config=thread)

current_state = graph.get_state(config=thread)

print('State after interrupt')
print(f'Response: {response}')
print(f'State: {current_state}')
print("\n\n")

# will perform the annotate action on the state
graph.update_state(
    config=thread,
    values={'data': [0.01, 0.02, 0.03]}
)

current_state = graph.get_state(config=thread)

print('State after update')
print(f'Response: {response}')
print(f'State: {current_state}')
print("\n\n")

response = graph.invoke(None, config=thread)

print('State after resume')
print(f'Response: {response}')
print(f'State: {current_state}')
print("\n\n")