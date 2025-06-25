from langgraph.graph import StateGraph, START, END
from pydantic import BaseModel

class InputState(BaseModel):
    input_value: int
    
class OutputState(BaseModel):
    output_value: int
    response: str
    
class InternalState(BaseModel):
    input_value: int
    additional_value: int
    output_value: int
    response: str
    
    
def input_node(state: InputState) -> InternalState:
    print("Processing Input Node")
    response = InternalState(
        input_value=state.input_value,
        additional_value=23,
        output_value=0,
        response=""
    )
    return response

def process_node(state: InternalState) -> InternalState:
    print("Processing Node 1")
    state.output_value = state.input_value + state.additional_value
    return state

def process_node_2(state: InternalState) -> InternalState:
    print("Processing Node 2")
    state.response = "The previous value was " + str(state.input_value) + " and the current value is " + str(state.output_value)
    return state

def output_node(state: InternalState) -> OutputState:
    print("Processing Output Node")
    response = dict()
    response["output_value"] = state.output_value 
    response["response"] = state.response
    return OutputState(**response)

graph = StateGraph(InputState, input=InputState, output=OutputState)

graph.add_node("input", input_node)
graph.add_node("process", process_node)
graph.add_node("process_2", process_node_2)
graph.add_node("output", output_node)

graph.add_edge(START, "input")
graph.add_edge("input", "process")
graph.add_edge("process", "process_2")
graph.add_edge("process_2", "output")
graph.add_edge("output", END)

compiled_graph = graph.compile()

response = compiled_graph.invoke({"input_value": 10})

print(response)