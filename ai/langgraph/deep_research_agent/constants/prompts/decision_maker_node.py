"""
Prompts for Decision maker node.
"""


from pydantic import BaseModel, Field
from typing import Literal, Optional


LLM_SERVICE_SYSTEM_PROMPT = """
"""


class llm_service_output_format(BaseModel):
    next_step: Literal['start_search', 'deep_dive'] = Field(description="")
    deep_dive_question: Optional[str] = Field(description="")
    start_search_question: Optional[str] = Field(description="")