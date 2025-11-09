"""
Node to perform human in loop.

Interacts with user to gather additional context or clarification.
"""

from langgraph.graph.state import Command
from configs.states import GraphOverallState


class HumanInteractionNode:
    """Human-in-the-loop node for user interaction.

    This node is where the graph pauses to wait for human input.
    When the user provides additional information, the flow returns
    to the decision maker to reassess the next steps.
    """

    def __call__(self, state: GraphOverallState) -> Command:
        """Execute human interaction step.

        This node doesn't modify the state - it simply routes back to the
        decision maker after the user has provided their input. The user's
        response will be added to the message history by the graph runtime.

        Args:
            state: Current graph state

        Returns:
            Command object directing back to decision_maker node
        """
        return Command(goto="decision_maker")
