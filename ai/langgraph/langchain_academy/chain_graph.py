from pydantic import BaseModel
from langgraph.graph import StateGraph, START, END, MessagesState
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import AnyMessage
from langgraph.graph.message import add_messages
from typing import Annotated
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


tools_list = [special_addition]

openai_model_with_tools = openai_model.bind_tools(tools_list)


# Custom message state
# class MessagesState(BaseModel):
#     messages: Annotated[list[AnyMessage], add_messages]

# Reuse langgraph's message state
# class MessagesState(MessagesState):
#     pass

# Langgraph's MessagesState isn't a pydantic model it's a dict, so we can't use . (dot) notation to access the messages
# We need to use ['messages'] to access the messages

def tool_call_node(state: MessagesState):
    response = openai_model_with_tools.invoke(
        input=state['messages']
    )
    
    print(f"Response: {response.content}")
    print(f"Tool calls: {response.tool_calls}")
    
    return {'messages': [response]}



builder = StateGraph(MessagesState)
builder.add_node("tool_call_node", tool_call_node)

builder.add_edge(START, "tool_call_node")
builder.add_edge("tool_call_node", END)

graph = builder.compile()

# graph.get_graph().draw_mermaid_png(output_file_path='graphs/chain_graph.png')

messages_from_template = prompt_template.invoke({'question': 'What is special addition of 10 and 10 ?'})
# OUTPUT: messages=[list of messages] -> [SystemMessage(), HumanMessage()]
# messages_from_template.messages -> list of messages
messages = messages_from_template.messages

response = graph.invoke(
    {
        'messages': messages
    }
)

# print(response['messages'][-1].pretty_print())

for message in response['messages']:
    print(message.pretty_print())