from langchain_core.tools import tool, InjectedToolArg
from langchain_openai import ChatOpenAI
import dotenv
from datetime import datetime, timedelta

dotenv.load_dotenv()

llm = ChatOpenAI(
    model='gpt-4.1-nano',
    temperature=0
)

# 1. Simple tool call

# create a tool
@tool
def get_current_local_time():
    """
    Returns the current local time.
    """

    return datetime.now().strftime('%H:%M:%S')


# bind tool to llm
tools_list = [get_current_local_time]

llm_with_tools = llm.bind_tools(tools_list)

# invoke llm with tool
response = llm_with_tools.invoke("What is the current local time ?")

# returns the tool calls response
print(response.tool_calls)
# [{'name': 'get_current_local_time', 'args': {}, 'id': 'call_vrqDTsYFo4eGrtIfs4NLFSdf', 'type': 'tool_call'}]

# tool can be invoke directly due to the tool decorator
args = response.tool_calls[0]['args']
print(get_current_local_time.invoke(args))


# 2. Special tool arguments

# 2.1 : InjectedToolArg - run time arguments allocation

@tool
def get_past_time_from_now(minutes: int, current_time: datetime = InjectedToolArg()):
    """
    Returns the time `minutes` minutes ago from the current time.
    """

    response = current_time - timedelta(minutes=minutes)
    return response


llm_with_tools = llm.bind_tools([get_past_time_from_now])

response = llm_with_tools.invoke("What was the time 3 hours ago ?")

print(response.tool_calls)

tool_args = response.tool_calls[0]['args']

# injecting run time args
tool_args['current_time'] = datetime.now()

print(get_past_time_from_now.invoke(tool_args))


#  3. Tools with artifacts

@tool(response_format='content_and_artifact')
def add_two_numbers(a: int, b: int) -> str:
    """
    Returns the sum of two numbers.
    """
    message_for_llm = f"The sum of {a} and {b} is {a + b}"
    additional_info = {
        'a': a,
        'b': b,
        'sum': a + b
    }

    return message_for_llm, additional_info


llm_with_tools = llm.bind_tools([add_two_numbers])

response = llm_with_tools.invoke("What is the sum of 2 and 3 ?")

print(response.tool_calls)
# [{
#     'name': 'add_two_numbers', 
#     'args': {'a': 2, 'b': 3}, 
#     'id': 'call_PeryHS7ZrGw9LEhz3uOdN8Bj',    -> required for artifacts
#     'type': 'tool_call'                       -> required for artifacts
# }]

tool_with_artifact_response = add_two_numbers.invoke(response.tool_calls[0])

print(tool_with_artifact_response)
# content='The sum of 2 and 3 is 5' name='add_two_numbers' tool_call_id='call_tuyWnSBfjS4s2q9fuKdvnSCB' artifact={'a': 2, 'b': 3, 'sum': 5}

print(f"Main response of tool: {tool_with_artifact_response.content}")  # main response of tool
print(f"Additional info of tool: {tool_with_artifact_response.artifact}")  # additional info of tool, can be used internally


# You can also invoke tool with only content 

tool_with_content_response = add_two_numbers.invoke(response.tool_calls[0]['args'])

print(tool_with_content_response)
# The sum of 2 and 3 is 5


# Dummy run for artifacts
response = add_two_numbers.invoke({'a': 6, 'b': 11})
# will contain only content, no artifact as id and type are not present
print(response)

response = add_two_numbers.invoke(
    {
        'args': {'a': 6, 'b': 11},
        'id': 'call_tuyWnSBfjS4s2q9fuKdvnSCB',
        'type': 'tool_call'
    }
)
print(response)