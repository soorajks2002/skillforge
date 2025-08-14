# MAIN TASK:
# Research assistant


from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage, SystemMessage
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import MessagesState
from pydantic import BaseModel, Field
from typing import Literal
from dotenv import load_dotenv
from typing import Annotated
from operator import add
from firecrawl import FirecrawlApp
import os
from langchain_core.messages import get_buffer_string

load_dotenv()

TOPIC = "The future of AI in the financial services industry"

llm = ChatOpenAI(model="gpt-5-nano-2025-08-07", temperature=1, reasoning_effort='low')
firecrawl_app = FirecrawlApp(api_key=os.getenv("FIRECRAWL_API_KEY"))

class Analyst(BaseModel):
    affiliation: str = Field(description="Primary affiliation of the analyst.")
    name: str = Field(description="Name of the analyst.")
    role: str = Field(description="Role of the analyst in the context of the topic.")
    description: str = Field(description="Description of the analyst focus, concerns, and motives.")

    @property
    def persona(self) -> str:
        return f"""Name: {self.name}\nRole: {self.role}\nAffiliation: {self.affiliation}\nDescription: {self.description}"""
    
class Perspectives(BaseModel):
    analysts: list[Analyst] = Field(description="Comprehensive list of analysts with their roles and affiliations.")
    
class AnalystState(BaseModel):
    topic: str = ""
    max_analysts: int = 3
    human_analyst_feedback: str = ""
    analysts: list[Analyst] = []
    
analyst_instructions="""You are tasked with creating a set of AI analyst personas. Follow these instructions carefully:

1. First, review the research topic:
{topic}
        
2. Examine any editorial feedback that has been optionally provided to guide creation of the analysts: 
        
{human_analyst_feedback}
    
3. Determine the most interesting themes based upon documents and / or feedback above.
                    
4. Pick the top {max_analysts} themes.

5. Assign one analyst to each theme."""


# Create analyst generation graph

def create_analyst(state: AnalystState) -> AnalystState:
    
    topic = state.topic
    human_analyst_feedback = state.human_analyst_feedback
    max_analysts = state.max_analysts
    
    system_prompt = analyst_instructions.format(
        topic=topic,
        human_analyst_feedback=human_analyst_feedback,
        max_analysts=max_analysts
    )
    
    structured_llm = llm.with_structured_output(Perspectives)
    
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content="Generate the set of analysts.")
    ]
    
    analysts = structured_llm.invoke(messages)
    
    state.analysts = analysts.analysts
    
    return state

def human_feedback(state: AnalystState) -> AnalystState:
    
    analysts = state.analysts
    
    for analyst in analysts:
        print(analyst.persona)
        print('-'*5)
    
    human_feedback = input("Please provide feedback on the analysts (n if no feedback): ")
    
    if human_feedback == 'n':
        human_feedback = ""
        
    state.human_analyst_feedback = human_feedback
    return state

def should_continue(state: AnalystState) -> Literal['create_analyst', END]:
    if state.human_analyst_feedback:
        return 'create_analyst'
    return END
    
analyst_graph_builder = StateGraph(AnalystState)
analyst_graph_builder.add_node('create_analyst', create_analyst)
analyst_graph_builder.add_node('human_feedback', human_feedback)

analyst_graph_builder.add_edge(START, 'create_analyst')
analyst_graph_builder.add_edge('create_analyst', 'human_feedback')
analyst_graph_builder.add_conditional_edges('human_feedback', should_continue, ['create_analyst', END])

analyst_graph = analyst_graph_builder.compile()
analyst_graph.get_graph(xray=1).draw_mermaid_png(output_file_path="mermaid_diagrams/research_assistant_analyst_graph.png")

test_state = AnalystState(topic=TOPIC)

output = analyst_graph.invoke(test_state)

# print("-- finalized analysts --")
analysts = output['analysts']
# for analyst in analysts:
#     print(analyst.persona)
#     print('-'*5)
# print(analysts)

# 2. Interview

class InterviewState(MessagesState):
    max_num_turns: int
    context: Annotated[list, add]
    analyst: Analyst
    interview: str
    sections: list
    
question_instructions = """You are an analyst tasked with interviewing an expert to learn about a specific topic. 

Your goal is boil down to interesting and specific insights related to your topic.

1. Interesting: Insights that people will find surprising or non-obvious.
        
2. Specific: Insights that avoid generalities and include specific examples from the expert.

Here is your topic of focus and set of goals: {goals}
        
Begin by introducing yourself using a name that fits your persona, and then ask your question.

Continue to ask questions to drill down and refine your understanding of the topic.
        
When you are satisfied with your understanding, complete the interview with: "Thank you so much for your help!"

Remember to stay in character throughout your response, reflecting the persona and goals provided to you."""


def generate_question(state: InterviewState) -> InterviewState:
    analyst = state["analyst"]
    messages = state["messages"]
    
    llm_messages = [SystemMessage(content=question_instructions.format(goals=analyst.persona))] + messages
    
    questions = llm.invoke(llm_messages)
    
    result = HumanMessage(content=questions.content)
    
    return {'messages': [questions]}


search_instructions = SystemMessage(content=f"""You will be given a conversation between an analyst and an expert. 

Your goal is to generate a well-structured query for use in retrieval and / or web-search related to the conversation.
        
First, analyze the full conversation.

Pay particular attention to the final question posed by the analyst.

Convert this final question into a well-structured web search query""")

class SearchQuery(BaseModel):
    search_query: str = Field(None, description="Search query for retrieval.")

def search_query(state: InterviewState) -> InterviewState:
    messages = state["messages"]
    
    llm_messages = [search_instructions] + messages
    
    query = llm.with_structured_output(SearchQuery).invoke(llm_messages)
    
    results = firecrawl_app.search(
        query=query.search_query,
        limit=1)
    
    context_str = str()
    context_str += f"Title: {results.data[0]['title']}\nDescription: {results.data[0]['description']}"
    
    return {'context': [context_str]}

answer_instructions = """You are an expert being interviewed by an analyst.

Here is analyst area of focus: {goals}. 
        
You goal is to answer a question posed by the interviewer.

To answer question, use this context:
        
{context}

When answering questions, follow these guidelines:
        
1. Use only the information provided in the context. 
        
2. Do not introduce external information or make assumptions beyond what is explicitly stated in the context.

3. The context contain sources at the topic of each individual document.

4. Include these sources your answer next to any relevant statements. For example, for source # 1 use [1]. 

5. List your sources in order at the bottom of your answer. [1] Source 1, [2] Source 2, etc
        
6. If the source is: <Document source="assistant/docs/llama3_1.pdf" page="7"/>' then just list: 
        
[1] assistant/docs/llama3_1.pdf, page 7 
        
And skip the addition of the brackets as well as the Document source preamble in your citation."""


def expert_answer_generation(state: InterviewState) -> InterviewState:
    messages = state["messages"]
    context = state["context"]
    analyst = state["analyst"]
    
    llm_messages = [
        SystemMessage(content=answer_instructions.format(
            goals=analyst.persona, 
            context=context))
        ] + messages
    
    answer = llm.invoke(llm_messages)
    answer.name = "expert"
    
    return {'messages': [answer]}

def save_interview(state: InterviewState):
    messages = state["messages"]
    interview = get_buffer_string(messages)
    return {"interview": interview}

def route_messages(state: InterviewState, 
                   name: str = "expert"):

    messages = state["messages"]
    max_num_turns = state.get('max_num_turns',2)
    
    num_responses = len(
        [m for m in messages if isinstance(m, AIMessage) and m.name == name]
    )

    if num_responses >= max_num_turns:
        return 'save_interview'

    last_question = messages[-2]
    
    if "Thank you so much for your help" in last_question.content:
        return 'save_interview'

    return "ask_question"


section_writer_instructions = """You are an expert technical writer. 
            
Your task is to create a short, easily digestible section of a report based on a set of source documents.

1. Analyze the content of the source documents: 
- The name of each source document is at the start of the document, with the <Document tag.
        
2. Create a report structure using markdown formatting:
- Use ## for the section title
- Use ### for sub-section headers
        
3. Write the report following this structure:
a. Title (## header)
b. Summary (### header)
c. Sources (### header)

4. Make your title engaging based upon the focus area of the analyst: 
{focus}

5. For the summary section:
- Set up summary with general background / context related to the focus area of the analyst
- Emphasize what is novel, interesting, or surprising about insights gathered from the interview
- Create a numbered list of source documents, as you use them
- Do not mention the names of interviewers or experts
- Aim for approximately 400 words maximum
- Use numbered sources in your report (e.g., [1], [2]) based on information from source documents
        
6. In the Sources section:
- Include all sources used in your report
- Provide full links to relevant websites or specific document paths
- Separate each source by a newline. Use two spaces at the end of each line to create a newline in Markdown.
- It will look like:

### Sources
[1] Link or Document name
[2] Link or Document name

7. Be sure to combine sources. For example this is not correct:

[3] https://ai.meta.com/blog/meta-llama-3-1/
[4] https://ai.meta.com/blog/meta-llama-3-1/

There should be no redundant sources. It should simply be:

[3] https://ai.meta.com/blog/meta-llama-3-1/
        
8. Final review:
- Ensure the report follows the required structure
- Include no preamble before the title of the report
- Check that all guidelines have been followed"""

def write_section(state: InterviewState):
    context = state["context"]
    analyst = state["analyst"]
    system_message = section_writer_instructions.format(focus=analyst.description)
    section = llm.invoke([
        SystemMessage(content=system_message),
        HumanMessage(content=f"Use this source to write your section: {context}")
        ]) 
    return {"sections": [section.content]}


interview_graph_builder = StateGraph(InterviewState)
interview_graph_builder.add_node('generate_question', generate_question)
interview_graph_builder.add_node('search_query', search_query)
interview_graph_builder.add_node('expert_answer_generation', expert_answer_generation)
interview_graph_builder.add_node('write_section', write_section)
interview_graph_builder.add_node('save_interview', save_interview)
interview_graph_builder.add_node('route_messages', route_messages)

interview_graph_builder.add_edge(START, 'generate_question')
interview_graph_builder.add_edge('generate_question', 'search_query')
interview_graph_builder.add_edge('search_query', 'expert_answer_generation')
interview_graph_builder.add_conditional_edges('expert_answer_generation', route_messages, ['save_interview', 'generate_question'])
interview_graph_builder.add_edge('save_interview', 'write_section')
interview_graph_builder.add_edge('write_section', END)

interview_graph = interview_graph_builder.compile()
interview_graph.get_graph(xray=1).draw_mermaid_png(output_file_path="mermaid_diagrams/research_assistant_interview_graph.png")

messages = [HumanMessage(f"So you said you were writing an article on {TOPIC}?")]

analyst_selected = analysts[0]
response = interview_graph.invoke({
    "analyst": analyst_selected,
    "messages": messages,
    "max_num_turns": 2
})

print(response)