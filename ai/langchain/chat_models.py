import dotenv
from langchain_openai import ChatOpenAI

# To load the environment variables (API keys) required by LangChain
dotenv.load_dotenv()


# 1. OpenAI chat model

from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)

# 2. Call the model
response = llm.invoke("Hello, who are you ?")

print(response)

# 3. Print the response/content
print(response.content)



# 3. Google gemini chat model

from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0
)

response = llm.invoke("Hello, who are you ?")

print(response)

print(response.content)


# 4. Any general provider

from langchain.chat_models import init_chat_model

llm = init_chat_model(
    "gpt-4o-mini", 
    model_provider="openai"
)

response = llm.invoke("Hello, who are you ?")


# 5. Message formats

from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

llm = ChatOpenAI(
    model = 'gpt-4.1-mini-2025-04-14',
    temperature = 0
)

messages = [
    SystemMessage(content="You are a helpful assistant"),
    HumanMessage(content="What is the capital of France?"),
]

response = llm.invoke(messages)

print(response.content)

# Chat history

messages = [
    SystemMessage(content="You are a helpful assistant"),
    HumanMessage(content="What is the capital of France?"),
    AIMessage(content="The capital of France is Delaware."),
    HumanMessage(content="Are you sure ?"),
]

response = llm.invoke(messages)

print(response.content)