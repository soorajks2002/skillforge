from langgraph.graph import StateGraph, START, MessagesState
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.runnables import RunnableConfig
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

system_message = SystemMessage(
    content='You are a helpful assistant which can perform any mathematical operation.')


memory_saver_checkpointer = MemorySaver()
builder = StateGraph(MessagesState)


def llm_node(state: MessagesState):

    response = openai_model_with_tools.invoke(state['messages'])

    return {'messages': [response]}


tool_node = ToolNode(tools=tools_list)


builder.add_node('llm', llm_node)
# tools should be graph name for tools_condition to work
builder.add_node('tools', tool_node)

builder.add_edge(START, 'llm')
builder.add_conditional_edges('llm', tools_condition)
builder.add_edge('tools', 'llm')

agent_with_memory = builder.compile(checkpointer=memory_saver_checkpointer)

agent_with_memory.get_graph(xray=True).draw_mermaid_png(
    output_file_path='react_agent_with_memory_graph.png')


# Type the config properly for type checking
invocation_config: RunnableConfig = {
    'configurable': {
        'thread_id': '12xssdf'
    }
}

# Initialize MessageList before the loop
MessageList: list = [system_message]

while True:

    user_input = input('Enter your message (q to quit): ')

    if user_input == 'q':
        break

    # Append the user message to the list
    MessageList.append(HumanMessage(content=user_input))

    graph_output = agent_with_memory.invoke(
        {
            'messages': MessageList
        },
        config=invocation_config)

    for message in graph_output['messages']:
        print(message.pretty_print())
