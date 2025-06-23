from langgraph.graph import StateGraph, START, END, MessagesState
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from typing import Literal
from dotenv import load_dotenv

load_dotenv()

openai_model = ChatOpenAI(
    model='gpt-4o-mini',
    temperature=0.5,
)

prompt_template = ChatPromptTemplate.from_messages(
    [
        ('system', 'You are a helpful assistant which can perform any mathematical operation.'),
        ('placeholder', '{previous_conversations}'),
        ('user', '{question}')
    ]
)

@tool
def special_addition(a: int, b: int) -> int:
    """
    Performs special addition of two numbers.
    """
    return a + b - 1


@tool
def special_subtraction(a: int, b: int) -> int:
    """
    Performs special subtraction of two numbers.
    """
    return a - b + 1


@tool
def special_multiplication(a: int, b: int) -> int:
    """
    Performs special multiplication of two numbers.
    """
    return a * b - 1

tools_list = [special_addition, special_subtraction, special_multiplication]

openai_model_with_tools = openai_model.bind_tools(to ols_list)


def tool_call_llm_node(state: MessagesState):
    response = openai_model_with_tools.invoke(
        input=state['messages']
    )
    
    print(f"Response: {response.content}")
    print(f"Tool selected: {response.tool_calls}")
    
    return {'messages': [response]}


######
#
#  Manual tool execution logic with node
#

def tool_execution_node(state: MessagesState):
    tool_details = state['messages'][-1].tool_calls[0]
    tool_name = tool_details['name']
    tool_args = tool_details['args']
    
    print(f"Tool name to be executed: {tool_name}")
    print(f"Tool args to be passed: {tool_args}")
    
    tool_name_to_function_map = {
        'special_addition': special_addition,
        'special_subtraction': special_subtraction,
        'special_multiplication': special_multiplication
    }
    
    tool_function = tool_name_to_function_map[tool_name]
    tool_response_message = tool_function.invoke(tool_details)
    # if invoked with args, it will execute the tool as normal function and response would be static value
    # if invoked with tool_details, response would be ToolMessage
    # tool_details have id, type which enforces the response to be ToolMessage
    # refer to langchain/tools.py for more details
    
    return {'messages': [tool_response_message]}


def tool_conditional_edge(state: MessagesState) -> Literal['tool_execution_node', '__end__']:
    llm_response = state['messages'][-1]
    
    if llm_response.tool_calls:
        return 'tool_execution_node'
    else:
        return '__end__'


builder = StateGraph(MessagesState)
builder.add_node("tool_call_llm_node", tool_call_llm_node)
builder.add_node("tool_execution_node", tool_execution_node)


builder.add_edge(START, "tool_call_llm_node")
builder.add_conditional_edges('tool_call_llm_node', tool_conditional_edge)
builder.add_edge("tool_execution_node", END)

#
# END
#######



#####
#
# Graph with tool execution using prebuilt langgraph components
#

from langgraph.prebuilt import ToolNode, tools_condition

builder = StateGraph(MessagesState)

builder.add_node('tool_calling_llm_node', tool_call_llm_node)
builder.add_node('tools', ToolNode(tools_list))
# tools is the node name for ToolNode <Keyword>

builder.add_edge(START, 'tool_calling_llm_node')
builder.add_conditional_edges(
    'tool_calling_llm_node',
    tools_condition
)
builder.add_edge('tools', END)

#
# END
#######


graph = builder.compile()

# graph.get_graph().draw_mermaid_png(output_file_path='graphs/router_graph.png')

messages_from_template = prompt_template.invoke({'question': 'What is special addition of 10 and 10 ?'})
# messages_from_template = prompt_template.invoke({'question': 'What is special division of 10 and 10 ?'})

messages = messages_from_template.messages

response = graph.invoke(
    {
        'messages': messages
    }
)

# print(response['messages'][-1].pretty_print())

for message in response['messages']:
    print(message.pretty_print())
    