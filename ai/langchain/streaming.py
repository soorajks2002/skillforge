from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableSequence
from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv


load_dotenv()

google_llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash-001",
    temperature=0,
)

messages = [
    HumanMessage(content="Generate a long 500 word story about a shoe.")
]


for chunk in google_llm.stream(messages):
    print(chunk.content, end="\n--\n")


generator_template = ChatPromptTemplate([
    ("system", "You are a helpful assistant which generates a long 100 word story about any topic."),
    ("human", "TOPIC: {topic}")
])

seq = RunnableSequence(
    generator_template,
    google_llm,
    StrOutputParser()
)

response = seq.stream({"topic": "A shoe"})

for chunk in response:
    print(chunk, end="\n--\n")
    