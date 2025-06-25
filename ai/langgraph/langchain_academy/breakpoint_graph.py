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

graph = builder.compile(interrupt_before=['node_3'], checkpointer=memory_saver)

graph.get_graph(xray=True).draw_mermaid_png(output_file_path="mermaid_diagrams/breakpoint_graph.png")


thread = {
    'configurable': {
        'thread_id': '123'
    }
}

response = graph.invoke(CustomState(data=[]), config=thread)

print(response)

print(graph.get_state(config=thread))
# StateSnapshot(values={'data': [1, 2]}, next=('node_3',), config={'configurable': {'thread_id': '123', 'checkpoint_ns': '', 'checkpoint_id': '1f050a0a-8061-6dec-8002-6a698dbccaf4'}}, metadata={'source': 'loop', 'writes': {'node_2': {'data': [2]}}, 'step': 2, 'parents': {}, 'thread_id': '123'}, created_at='2025-06-24T02:12:19.244787+00:00', parent_config={'configurable': {'thread_id': '123', 'checkpoint_ns': '', 'checkpoint_id': '1f050a0a-8060-6d7a-8001-d411f2f7e173'}}, tasks=(PregelTask(id='ee075af9-dcac-ea87-43ea-83f53b5398df', name='node_3', path=('__pregel_pull', 'node_3'), error=None, interrupts=(), state=None, result=None),), interrupts=())


# Re-run the graph with None (as input) with the same thread_id, it will resume from the breakpoint

continue_input = input("Do you want to continue ? (y/n)")

if continue_input == 'y':
    print("Resuming from the breakpoint")
    response = graph.invoke(None, config=thread)

print(response)