from langchain_core.messages import RemoveMessage, AIMessage, HumanMessage
from langgraph.graph.message import add_messages

messages_left = list()
messages_left.append(HumanMessage(content="This is first message."))

messages_right = list()
messages_right.append(AIMessage(content="This is second message."))

response = add_messages(
    messages_left,
    messages_right,
)

print(response)


# Each message object has a unique id.
# Using add_messages and id we can update or remove messages from a existing list of messages.


#  Rewriting / Updating message
messages_left = list()
messages_left.append(HumanMessage(content="This is first message.", id="1"))

print(messages_left)

messages_right = list()
messages_right.append(AIMessage(content="This is second message.", id="1"))

response = add_messages(
    messages_left,
    messages_right,
)

print("Message after updating.")
print(response)


#  Removing message
messages_left = list()
messages_left.append(HumanMessage(content="This is first message.", id="1"))
messages_left.append(HumanMessage(content="This is second message.", id="2"))
messages_left.append(HumanMessage(content="This is third message.", id="3"))
messages_left.append(HumanMessage(content="This is fourth message.", id="4"))
messages_left.append(HumanMessage(content="This is fifth message.", id="5"))
messages_left.append(HumanMessage(content="This is sixth message.", id="6"))

print(messages_left)

messages_to_delete = [RemoveMessage(id=str(i)) for i in range(3, 6)]

print("Messages to delete.")
print(messages_to_delete)

response = add_messages(messages_left, messages_to_delete)

print("Message after removing ids from 3 to 5.")
print(response)