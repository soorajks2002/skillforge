from langchain_openai import ChatOpenAI
import dotenv

dotenv.load_dotenv()

llm = ChatOpenAI(
    model = 'gpt-4.1-nano',
    temperature = 0
)

# 1. Simple structured output - Json body

# update model to use structured output
llm_with_structured_output = llm.with_structured_output(method='json_mode')

response = llm_with_structured_output.invoke("What is the structure of top level executive in a company? Response must be in json format.")

# with_structured_output returns a dict in response rather than full llm response
print(response)


# 2. Json schema based structured output

# Pydantic schema : better for validation

from pydantic import BaseModel, Field

class AnswerFormat(BaseModel):
    """
    Answer format for all the questions.
    """
    answer : str = Field(description="Answer to the question")
    reasoning : str = Field(description="Reasoning process to arrive at the answer")
    

llm_with_structured_output = llm.with_structured_output(AnswerFormat)

response = llm_with_structured_output.invoke("Which planet is closest to the farthest moon of jupiter?")

# returns the pydantic model instance, unlike a direct dict as above
# doesn't returns the full llm response
print(response)

# you can directly access the fields
print(response.answer)
print(response.reasoning)
