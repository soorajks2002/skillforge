"""
"""


from langchain_openai import ChatOpenAI
import os


API_KEY = os.getenv('OPENAI_API_KEY', '')


class LangChainOpenAILLMService:

    def __init__(self, model_name, use_responses_api=True):
        self.model_name = model_name
        self.use_responses_api = use_responses_api


    def get_model(self):
        return ChatOpenAI(
            model=self.model_name,
            temperature=0.6,
            max_completion_tokens=20000,
            use_responses_api=self.use_responses_api,
            api_key=API_KEY
        )
