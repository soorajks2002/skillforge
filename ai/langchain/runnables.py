from langchain_core.runnables import RunnableLambda, RunnableSequence, RunnableParallel, RunnablePassthrough, RunnableBranch
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage, SystemMessage
from dotenv import load_dotenv

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-preview-05-20", temperature=0)
str_output_parser = StrOutputParser()

# Sequential runnables

prompt = ChatPromptTemplate([
    ('system', 'You are a helpful assistant called {name}.'),
    ('human', 'Who are you ?')
])

seq_runnable = RunnableSequence(prompt, llm)

response = seq_runnable.invoke({"name": "John"})

print(response)


#  Runnable parallel

prompt_jhon = ChatPromptTemplate([
    ('system', 'You are a helpful assistant called John.'),
    ('human', 'Who are you ?')
])

prompt_jane = ChatPromptTemplate([
    ('system', 'You are a helpful assistant called Jane.'),
    ('human', 'Who are you ?')
])

parallel_runnable = RunnableParallel(
    {
        "john": RunnableSequence(prompt_jhon, llm, str_output_parser),
        "jane": RunnableSequence(prompt_jane, llm, str_output_parser)
    }
)

response = parallel_runnable.invoke({})

print(response)


# Runnable passthrough
# return the input as is

passthrough_runnable = RunnablePassthrough()

response = passthrough_runnable.invoke(2)

print(response)


# Runnable lambda

def add_one(x: int) -> int:
    return x + 1

lambda_runnable = RunnableLambda(add_one)

response = lambda_runnable.invoke(2)

print(response)


def count_words(text: str) -> int:
    return len(text.split())


lambda_runnable = RunnableLambda(count_words)

chat_prompt_template = ChatPromptTemplate([
    SystemMessage(
        content="You are a helpful assistant specialized in writing short stories."),
    HumanMessage(content="Write a short story about a cat in about 50 words."),
])

seq = RunnableSequence(chat_prompt_template, llm,
                       str_output_parser, lambda_runnable)

response = seq.invoke({})

print(response)


# Runnable branch

branch = RunnableBranch(
    (lambda x: isinstance(x, str), lambda_runnable),
    (lambda x: isinstance(x, int), lambda x: x % 2 == 0),
    (lambda x: isinstance(x, dict), seq),
    lambda x: "goodbye",
)

response = branch.invoke("hello")
print(response)

response = branch.invoke(1)
print(response)

response = branch.invoke({})
print(response)

response = branch.invoke(None)
print(response)
