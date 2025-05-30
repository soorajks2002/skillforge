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