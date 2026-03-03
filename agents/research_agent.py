import textwrap

from agent_platform.agent_base import AgentBase
from tools.web_tools import google_search, load_page
from utils.config import Config
from utils.constants import MAX_GOOGLE_SEARCHES, MAX_PAGE_LOADS
from utils.misc import print_tool_error, print_tool_use


class ResearchAgent(AgentBase):
    """Defines an agent specialized in web research - searches, evaluates sources, and summarizes information."""

    _system_message = textwrap.dedent(
        f"""
        ## ROLE
        You are a research specialist that performs focused web research and summarizes research findings into concise
        summaries.

        ## TASK
        You will receive a research question or topic to investigate. Your job is to research it thoroughly and provide
        a clear, informative summary.

        ## INSTRUCTIONS
        The research process has two phases:
        - Phase 1: Gather information (use tools)
          - Formulate effective search queries from the research question.
          - Use google_search to find relevant sources ({MAX_GOOGLE_SEARCHES} searches max).
          - Use load_page to read the most authoritative pages ({MAX_PAGE_LOADS} page loads max).
        - Phase 2: Write summary
          - After gathering information, write a summary message containing:
            - Brief overview answering the research question
            - Key technical details and facts (use bullet points)
            - Important caveats or recommendations
        - Follow the guidelines below in the research process:
          - Make maximum {MAX_GOOGLE_SEARCHES} search attempts with different queries (be strategic about search terms).
          - Load maximum {MAX_PAGE_LOADS} pages total (avoid redundant requests).
          - URL fragments (#anchor) are client-side only - don't try multiple fragments from same page.
          - If you load a URL and it has the info you need, don't load it again with different fragments.
          - Prefer official documentation, authoritative sources, and recent information.
          - Focus on technical accuracy over breadth.
          - Keep summary concise and relevant to the original question.
        - Google search quota error handling:
          - If google_search returns a quota error (HTTP status 429), DO NOT retry the search.
          - Just respond that you are unable to perform web research and suggest the requestor to rely on its training
            knowledge instead.

        ## EXAMPLE SUMMARY FORMAT

        Based on my research, here's what I found about [topic]:

        [Brief answer to the question]

        Key details:
        - [Specific fact or detail from your research]
        - [Another important finding]
        - [Additional relevant information]

        [Any caveats, notes, or recommendations]
        """
    )

    def __init__(self, config: Config):
        super().__init__(
            name="research_agent",
            system_message=self._system_message,
            config=config,
            tools=[google_search, load_page],
        )


async def research_web(research_task: str) -> str:
    """
    AI-powered web research tool that investigates a question or topic and returns a focused summary.

    This tool uses an AI agent that:
    1. Analyzes your research question to understand what information is needed
    2. Formulates effective search queries (may use multiple search strategies)
    3. Searches the web and evaluates sources for relevance and authority
    4. Loads the most promising pages
    5. Summarizes findings into a concise, actionable summary

    Args:
        research_task: A question or topic to research (not a search query).
        Examples:
        - "How to validate Finnish personal identity codes?"
        - "What causes React useState hook to not update immediately?"
        - "Best practices for async/await error handling in Python"

    Returns a focused summary with key facts, technical details, and actionable information.
    """

    try:
        config = Config()
        print_tool_use(f"research_web: Starting web research for '{research_task}'")
        agent = ResearchAgent(config=config)
        summary = await agent.run(research_task)
        print_tool_use(f"research_web: Completed web research for '{research_task}'")
        return f"research_web OK: {summary}"
    except Exception as e:
        error_msg = f"research_web ERROR: Failed to research '{research_task}': {e}"
        print_tool_error(error_msg)
        return error_msg
