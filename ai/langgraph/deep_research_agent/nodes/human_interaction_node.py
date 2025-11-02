"""
Node to perform human in loop.

Interacts with user.
"""


from langgraph.graph.state import Command
from configs.states import GraphOverallState



class HumanInteractionNode:
    
    def __call__(self, state:GraphOverallState) -> Command:
        
        return Command('decision_maker')