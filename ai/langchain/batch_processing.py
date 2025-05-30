from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableSequence
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()

google_llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash-001",
    temperature=0,
    )


generator_template = ChatPromptTemplate([
    ("system", "You are a helpful assistant which generates a short 10-100 word story about any topic. And a 200 word story if topic is either a dog or a cat. Strictly follow the word limit."),
    ("human", "TOPIC: {topic}")
])


seq = RunnableSequence(
    generator_template,
    google_llm,
    StrOutputParser()
)


results = seq.batch(
    [
        {"topic": "Dog"},
        {"topic": "Cat"},
        {"topic": "Shoe"},
        {"topic": "Fish"},
        {"topic": "Boat"},
        {"topic": "Car"},
    ]
)

for result in results:
    print(result)
    print("-" * 100)
    
    
results = seq.batch_as_completed(
    [
        {"topic": "Dog"},
        {"topic": "Cat"},
        {"topic": "Shoe"},
        {"topic": "Fish"},
    ]
)

for result in results:
    print(result)
    print("-" * 100)
    

#  .batch()
#  returns response of all in sequential order


#  .batch_as_completed()
#  returns response as they are completed, not in sequential order
#  response is tuple of (index, response)

# Response of above test
# (3, 'Finley the fish ...')
# ----------------------------------------------------------------------------------------------------
# (4, 'The old wooden boat ...')
# ----------------------------------------------------------------------------------------------------
# (2, "The old shoe sat on the porch, ...")
# ----------------------------------------------------------------------------------------------------
# (5, 'The old car, ....')
# ----------------------------------------------------------------------------------------------------
# (1, 'Whiskers twitched, ...')
# ----------------------------------------------------------------------------------------------------
# (0, "Barnaby, a scruffy ...")
# ----------------------------------------------------------------------------------------------------