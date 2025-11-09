"""
Prompts for Report Generation node.
"""

LLM_SERVICE_USER_PROMPT = """Based on all the search results provided above from multiple sources (Exa AI, Firecrawl, Google Search, and Tavily), 
please create a comprehensive research report.

Your report should:

1. **Synthesize Information**: Combine insights from all search sources to provide a complete picture
2. **Structure Clearly**: Use clear headings and sections to organize the information logically
3. **Cite Sources**: When possible, reference which search service provided key information
4. **Highlight Key Findings**: Emphasize the most important and relevant discoveries
5. **Be Comprehensive**: Cover all major aspects discovered in the research
6. **Maintain Accuracy**: Only include information that was found in the search results
7. **Identify Gaps**: If important information is missing, note what couldn't be found

Report Structure:
- Executive Summary: Brief overview of key findings
- Main Findings: Detailed information organized by topic/theme
- Sources and References: Note which search engines provided the most valuable information
- Conclusion: Summarize the overall insights

Make the report informative, well-organized, and easy to read. Use markdown formatting for better readability."""