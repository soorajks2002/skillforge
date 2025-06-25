from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph.message import add_messages, MessagesState
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, RemoveMessage, SystemMessage
import dotenv

dotenv.load_dotenv()

gemini_client = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.7
)

def simulate_system_prompt_node(message_state):
    response = {'messages': [SystemMessage("You are a helpful assistant that performs math operations")]}
    return response

def simulate_user_prompt_node(message_state):
    response = {'messages': [HumanMessage("Add 10 and 20")]}
    return response

def llm_maths_node(message_state):
    messages = message_state.get("messages", [])
    
    response = gemini_client.invoke(messages)
    
    return {"messages": [response]}

builder = StateGraph(MessagesState)

builder.add_node("simulate_system_prompt", simulate_system_prompt_node)
builder.add_node("simulate_user_prompt", simulate_user_prompt_node)
builder.add_node("llm_maths", llm_maths_node)

builder.add_edge(START, "simulate_system_prompt")
builder.add_edge("simulate_system_prompt", "simulate_user_prompt")
builder.add_edge("simulate_user_prompt", "llm_maths")
builder.add_edge("llm_maths", END)

memory = MemorySaver()
graph = builder.compile(checkpointer=memory)

thread = {"configurable": {"thread_id": "1"}}

message_input = []

response = graph.invoke({'messages': message_input}, config=thread)

print("Default, add 10 and 20\n--\n")
print(response['messages'][-1].content)

# get_state returns the current state of the graph (the state at the latest node which ran)
current_state = graph.get_state(thread)
print("\n--\n")
print(current_state)

print("\n\n---\n\n")
# get_state_history returns all the states of all the nodes that ran in a specific thread
# all_states = [s for s in graph.get_state_history(thread)]
all_states = [s.next for s in graph.get_state_history(thread)]
print(all_states)
print("\n\n---\n\n")



######
#
# NOW, LET's edit the states of the thread and rerun the graph but with updated human message
# Add -1 and 1
#
######


# we will keep the last node to be the human simulation node and latter update the state of the node with new value
# the states are managed as a stack, so the last state is the first one in the list
all_states = [s for s in graph.get_state_history(thread)]
new_start_state = all_states[1:]

node_state_to_update = new_start_state[0]

print(f"Next node to call: {node_state_to_update.next}")

for message in node_state_to_update.values['messages']:
    print("--\n")
    print(message.content)
    print(message.id)

# update_state 
# updates the existing state, if config only has thread_id
# but if config contains a checkpoint_id as well then it will create a new fork and update will also be applied to a new checkpoint not the existing one
# if as_node isn't provided, then the state will be updated in the current node or else it will be updated in the node specified by as_node

print(" First will update state by removing the last human message")
message_to_remove = node_state_to_update.values['messages'][-1]

print(f"Message to remove: {message_to_remove.content}")
print(f"Last message id: {message_to_remove.id}")

removed_message_fork_checkpoint = graph.update_state(
    config=node_state_to_update.config,
    values={'messages': [RemoveMessage(id=message_to_remove.id)]}
)

removed_message_fork_state = graph.get_state(config=removed_message_fork_checkpoint)

print("Messages after removing the last human message")

for message in removed_message_fork_state.values['messages']:
    print("--\n")
    print(message.content)
    print(message.id)

print("\n\n---\n\n")

print("Now will update the new state by adding a new human message")
message_to_add = HumanMessage(content="Add -1 and 1")

new_added_message_fork = graph.update_state(
    config=removed_message_fork_checkpoint,
    values={'messages': [message_to_add]}
)

new_added_message_fork_state = graph.get_state(config=new_added_message_fork)

print("Messages after adding a new human message")

for message in new_added_message_fork_state.values['messages']:
    print("--\n")
    print(message.content)
    print(message.id)

print("\n\n---\n\n")


print("Now will invoke the same thread with the new state and updated checkpoint")

response = graph.invoke(None, config=new_added_message_fork)


print("---")
for message in response['messages']:
    print(message.pretty_print())