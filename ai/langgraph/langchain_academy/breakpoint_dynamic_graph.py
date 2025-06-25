from langgraph.graph import StateGraph, START, END
from typing import TypedDict, List, Annotated
from operator import add
from langgraph.checkpoint.memory import MemorySaver
from langgraph.errors import NodeInterrupt
from langgraph.graph.message import add_messages

class CustomState(TypedDict):
    data: Annotated[List[int], add]
    
    
def node_1(state: CustomState) -> CustomState:
    return CustomState(data=[1])

def node_2(state: CustomState) -> CustomState:
    if len(state['data']) < 1:
        # NodeInterrupt is a special exception that is used to interrupt the graph
        # Very similar to interrupt_before and interrupt_after in the compile function
        # Catch here is that the next state would be the current node itself, not its successor
        # Forcing the graph to resume from the current node, and fix the exception
        raise NodeInterrupt("Invalid initial state was provided")
    
    return CustomState(data=[2])

def node_3(state: CustomState) -> CustomState:
    return CustomState(data=[3])


builder = StateGraph(CustomState)

builder.add_node('node_1', node_1)
builder.add_node('node_2', node_2)
builder.add_node('node_3', node_3)

builder.add_edge(START, 'node_1')
builder.add_edge('node_1', 'node_2')
builder.add_edge('node_2', 'node_3')
builder.add_edge('node_3', END)

memory_saver = MemorySaver()
graph = builder.compile(interrupt_before=['node_2'], checkpointer=memory_saver)
graph.get_graph(xray=True).draw_mermaid_png(output_file_path="mermaid_diagrams/dynamic_breakpoint_graph.png")

print("Incorrect state.")

input_state = CustomState(data=[])

thread = {
    'configurable': {
        'thread_id': '123'
    }
}

response = graph.invoke(input_state, config=thread)
print(response)

current_state = graph.get_state(config=thread)

print(current_state)
print(f"\n Next node: {current_state.next}")

print("\n\n---\nState after updating")
graph.update_state(
    config=thread,
    values={'data': [0.1, 0.2]}
)

current_state = graph.get_state(config=thread)

print(current_state)
print(f"\n Next node: {current_state.next}")


print("\n\n---\nUpdating the initial value by overriding the state\n---\n")

response = graph.invoke(None, config=thread)
print(response)
print("\n\n")
print(graph.get_state(config=thread))