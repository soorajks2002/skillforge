from mailbox import Message
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import MessagesState
from langchain_google_genai import ChatGoogleGenerativeAI
import dotenv
from langchain_core.messages import HumanMessage, RemoveMessage, SystemMessage
from langgraph.checkpoint.memory import MemorySaver
from typing import Literal

dotenv.load_dotenv()

google_llm_client = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
)

memory_saver = MemorySaver()

class MessageStateWithSummary(MessagesState):
    summary: str
    
def summarization_node(state: MessageStateWithSummary) -> MessageStateWithSummary:
    
    human_message = HumanMessage("Create a summary of the conversation so far.")
    
    if state['summary']:
        human_message = HumanMessage(f"This is the summary of the conversation so far: {state['summary']}, Extend it with the conversation so far.")
        
    messages = state['messages'] + [human_message]
    
    response = google_llm_client.invoke(messages)
    
    messages_to_remove = [RemoveMessage(id=message.id) for message in state['messages']]
    
    print('-'*10)
    print(response.content)
    print('-'*10)
    
    return MessageStateWithSummary(
        messages=messages_to_remove,
        summary=response.content,
    )
    
    
def chat_node(state: MessageStateWithSummary) -> MessageStateWithSummary:
    
    if state['summary']:
        system_message = SystemMessage(f"This is the summary of the conversation so far: {state['summary']}")
        messages = [system_message] + state['messages']
    else:
        messages = state['messages']
        
    response = google_llm_client.invoke(messages)
    
    return {'messages': [response]}


def should_summarize(state: MessageStateWithSummary) -> Literal['summarize', END]:
    
    if len(state['messages']) > 4:
        return "summarize"
    
    return END


builder = StateGraph(MessageStateWithSummary)

builder.add_node('chat', chat_node)
builder.add_node('summarize', summarization_node)

builder.add_edge(START, 'chat')
builder.add_conditional_edges('chat', should_summarize)
builder.add_edge('summarize', END)

graph = builder.compile(checkpointer=memory_saver)
graph.get_graph(xray=True).draw_mermaid_png(output_file_path="mermaid_diagrams/chatbot_with_summarization_graph.png")


configure = {
    'configurable': {
        'thread_id': '123'
    }
}

response = graph.invoke(
    {'messages': [HumanMessage('Hello, how are you ?')], 'summary': ''},
    config=configure
)

for message in response['messages']:
    print(message.pretty_print())
    
    
response = graph.invoke(
    {'messages': HumanMessage('How far is the moon from the earth ?')},
    config=configure
)

for message in response['messages']:
    print(message.pretty_print())
    
    
response = graph.invoke(
    {'messages': HumanMessage('What is the capital of France ?')},
    config=configure
)

for message in response['messages']:
    print(message.pretty_print())
    
    
response = graph.invoke(
    {'messages': HumanMessage('Which asteroid belt is closest to the sun ?')},
    config=configure
)

for message in response['messages']:
    print(message.pretty_print())
    
    
response = graph.invoke(
    {'messages': HumanMessage('About what all planets have we talked so far ?')},
    config=configure
)

for message in response['messages']:
    print(message.pretty_print())