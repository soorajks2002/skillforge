"""

"""


from typing import List

from langchain_core.messages import AIMessage, AnyMessage, HumanMessage
from configs.states import GraphOverallState
from constants.prompts.report_generation_node import LLM_SERVICE_USER_PROMPT
from clients.langchain_openai_client import LangChainOpenAILLMService


class ReportGenerationNode:
    
    def llm_response(self, messages:List[AnyMessage]) -> AIMessage:
        chat_model = LangChainOpenAILLMService(model_name='gpt-5').get_model()
        
        messages.append(HumanMessage(content=LLM_SERVICE_USER_PROMPT))
        
        response = chat_model.invoke(messages)
        
        return response
    
    def __call__(self,state:GraphOverallState) -> GraphOverallState:
        messages = state['messages']
        
        llm_response = self.llm_response(messages)
        
        return {'messages': [llm_response]}