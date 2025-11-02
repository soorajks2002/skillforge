"""
State configs for the deep research agent graph.

Uses TypedDict as base instead of pydantic.
"""


from langgraph.graph import MessagesState


class GraphInputState(MessagesState):
    pass
    
class GraphOutputState(MessagesState):
    pass
    
class GraphOverallState(MessagesState):
    pass