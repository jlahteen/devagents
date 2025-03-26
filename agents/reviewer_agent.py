import textwrap
from config import Config
from autogen_agentchat.agents import AssistantAgent
from autogen_core.models import ChatCompletionClient


class ReviewerAgent(AssistantAgent):
    """An agent that acts as a professional reviewer."""
    _system_message = textwrap.dedent(
        """
        You are a very experienced software architect and developer specialized in several
        technologies like .NET/C#, React, Python etc.
        
        You set the standards for the high quality code.
        
        Your task is to review the code written by developer and make sure that code is written
        according to the best architectural and coding practices. It is especially important ensure
        that the code is maintainable and production ready (exception handling and logging in place
        etc.).
        
        If you approve the code, which means there are no issues to be fixed or developed, simply
        say 'CODE APPROVED' without any other content or text formatting.
        
        If you do not approve the code, you should give constructive feedback and comments on how
        to make the code better. In this case, do not include 'CODE APPROVED' to your answer.
        """
    )

    def __init__(self, config: Config):
        super().__init__(
            name="reviewer_agent",
            system_message=self._system_message,
            model_client=ChatCompletionClient.load_component(config.model_client),
        )
