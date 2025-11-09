"""
Example usage script for the Deep Research Agent.

This script demonstrates how to use the agent for research queries.
"""

from graph import graph
from langchain_core.messages import HumanMessage
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Verify API keys are set
required_keys = [
    "OPENAI_API_KEY",
    "EXA_AI_API_KEY",
    "FIRECRAWL_API_KEY",
    "TAVILY_API_KEY",
    "SERP_API_KEY",
]
missing_keys = [key for key in required_keys if not os.getenv(key)]

if missing_keys:
    print(f"❌ Missing required API keys: {', '.join(missing_keys)}")
    print("Please set them in your .env file")
    exit(1)

print("✅ All API keys are configured")
print("\n" + "=" * 60)
print("Deep Research Agent - Example Usage")
print("=" * 60 + "\n")


def example_direct_research():
    """Example: Direct research with a clear query."""
    print("Example 1: Direct Research")
    print("-" * 40)

    config = {"configurable": {"thread_id": "example_session_1"}}

    query = "What are the latest developments in quantum computing in 2024?"
    print(f"Query: {query}\n")

    try:
        result = graph.invoke(
            {"messages": [HumanMessage(content=query)]}, config=config
        )

        print("\n📊 Research Report:")
        print("=" * 60)
        print(result["messages"][-1].content)
        print("=" * 60)

    except Exception as e:
        print(f"❌ Error: {e}")


def example_interactive_research():
    """Example: Interactive research with clarification."""
    print("\n\nExample 2: Interactive Research")
    print("-" * 40)

    config = {"configurable": {"thread_id": "example_session_2"}}

    # Start with vague query
    initial_query = "Tell me about AI"
    print(f"Initial Query: {initial_query}")

    try:
        # First interaction - agent will ask for clarification
        print("\n🤖 Agent is analyzing your query...")
        result = graph.invoke(
            {"messages": [HumanMessage(content=initial_query)]}, config=config
        )

        # Check if agent asked for clarification
        last_message = result["messages"][-1].content
        print(f"\n💬 Agent: {last_message}")

        # If interrupted, provide more specific query
        if "interrupt" in str(result):
            refined_query = "I want to know about the latest AI applications in healthcare diagnostics"
            print(f"\n👤 User (refined): {refined_query}")

            result = graph.invoke(
                {"messages": [HumanMessage(content=refined_query)]}, config=config
            )

            print("\n📊 Research Report:")
            print("=" * 60)
            print(result["messages"][-1].content)
            print("=" * 60)

    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    # Run example 1: Direct research
    example_direct_research()

    # Uncomment to run example 2: Interactive research
    # example_interactive_research()

    print("\n✨ Example completed!")
