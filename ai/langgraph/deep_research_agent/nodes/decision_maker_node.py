"""
Main Node for the agent.
Decides and finalizes the plan for any new question.
"""


from typing import Any, Dict, List, Tuple
from langchain_core.messages import AIMessage, AnyMessage, SystemMessage, ToolMessage
from langchain_core.messages.tool import ToolCall
from langgraph.graph.state import Command
from configs.states import GraphOverallState
from constants.prompts.decision_maker_node import LLM_SERVICE_SYSTEM_PROMPT, llm_service_output_format
from clients.langchain_openai_client import LangChainOpenAILLMService
from langgraph.graph.message import add_messages


class DecisionMakerNode:
    """
    """

    def pre_process(self, messages:List[AnyMessage]) -> List[AnyMessage]:

        non_tool_messages = []

        for message in messages:
            if isinstance(message, ToolMessage):
                continue

            non_tool_messages.append(message)

        return non_tool_messages

    def llm_response(self, messages:List[AnyMessage]) -> Dict:
        llm_messages: List[AnyMessage] = [SystemMessage(LLM_SERVICE_SYSTEM_PROMPT)]
        llm_messages.extend(messages)
        
        chat_model = LangChainOpenAILLMService(model_name='gpt-5-nano').get_model()
        chat_model = chat_model.with_structured_output(llm_service_output_format)
        
        response = chat_model.invoke(llm_messages)
        
        return response

    def post_process(self, response:llm_service_output_format) -> Tuple[str, AIMessage]:
        
        next_step = response.next_step
        
        if next_step == 'human_in_loop':
            deep_dive_question = response.deep_dive_question
            tool_message = AIMessage(content=deep_dive_question)
            
            return 'human', tool_message
        
        start_search_question = response.start_search_question
        tool_message = AIMessage(
            content=f"Starting deep research on {start_search_question}",
            tool_calls = {
                "name": "combined_search_tool", 
                "args": {"query": start_search_question}, 
                "id": "123"
            }
        )
            
        return 'start_search', tool_message
        

    def __call__(self,
        state:GraphOverallState
    ) -> Command:

        messages = state['messages']

        cleaned_messages = self.pre_process(messages)

        llm_response = self.llm_response(cleaned_messages)

        next_node, tool_message = self.post_process(llm_response)
        
        add_messages(state['messages'], [tool_message])

        return Command(next_node, state)
