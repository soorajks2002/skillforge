from langgraph.graph import StateGraph, START, END, MessagesState
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import SystemMessage, HumanMessage
import dotenv

dotenv.load_dotenv()

openai_model = ChatOpenAI(
    model='gpt-4o-mini'
)

@tool
def special_addition(a: float, b: float) -> float:
    """
    This tool is used to perform special addition of two numbers.
    """
    return a + b + (a/b)

@tool
def special_subtraction(a: float, b: float) -> float:
    """
    This tool is used to perform special subtraction of two numbers.
    """
    return a - b - ((a+b)/b)

@tool
def special_multiplication(a: float, b: float) -> float:
    """
    This tool is used to perform special multiplication of two numbers.
    """
    return (a * b) + (b/a)

tools_list = [special_addition, special_subtraction, special_multiplication]

openai_model_with_tools = openai_model.bind_tools(tools_list)

MessageList = [
    SystemMessage(content='You are a helpful assistant which can perform any mathematical operation.')
]

graph = StateGraph(MessagesState)


def llm_node(state: MessagesState):
    
    response = openai_model_with_tools.invoke(state['messages'])
    
    return {'messages': [response]}


tool_node = ToolNode(tools=tools_list)


graph.add_node('llm', llm_node)
graph.add_node('tools', tool_node) # tools should be graph name for tools_condition to work

graph.add_edge(START, 'llm')
graph.add_conditional_edges('llm', tools_condition)
graph.add_edge('tools', 'llm')

compiled_graph = graph.compile()

# compiled_graph.get_graph(xray=True).draw_mermaid_png(output_file_path='mermaid_graphs/react_agent_graph.png')

MessageList.append(
    HumanMessage(content='Calculate the special addition of 9 and 10 then compute the special multiplication of it with 61 and at last perform the special subtraction of the result with 100')
)


graph_output = compiled_graph.invoke({
    'messages': MessageList
})


for message in graph_output['messages']:
    print(message.pretty_print())