from langchain_core.prompts import PromptTemplate, ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

# Simple prompt template

prompt = PromptTemplate.from_template(
    "You are a helpful assistant called {name}."
)

formatted_prompt = prompt.invoke({"name": "John"})

print(formatted_prompt)



#  Chat prompt template

# OpenAI format key value
prompt = ChatPromptTemplate(
    [
        ('system', 'You are a helpful assistant called {name}'),
        ('user', 'What is your name ?'),
        ('assistant', 'Let me think ...')
    ]
)

# Langchain format key value
prompt = ChatPromptTemplate(
    [
        ('system', 'You are a helpful assistant called {name}'),
        ('human', 'What is your name ?'),
        ('ai', 'Let me think ...')
    ]
)

formatted_prompt = prompt.invoke({"name": "John"})

print(formatted_prompt)


# Message placeholder

prompt = ChatPromptTemplate.from_messages([
    ('system', 'You are a helpful assistant called {name}'),
    MessagesPlaceholder("history"),
    ('human', 'What is your name ?')
])

# placeholder key value
prompt = ChatPromptTemplate.from_messages([
    ('system', 'You are a helpful assistant called {name}'),
    ('placeholder', "{history}"),
    ('human', 'What is your name ?')
])


history = [
    HumanMessage(content="What task are you tasked to perform ?"),
    AIMessage(content="I am tasked to help you with everything."),
]

formatted_prompt = prompt.invoke({"name": "John", "history": history})

print(formatted_prompt)