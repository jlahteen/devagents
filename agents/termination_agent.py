import textwrap

from autogen_agentchat.agents import AssistantAgent
from autogen_core.models import ChatCompletionClient

from config import Config


class TerminationAgent(AssistantAgent):
    """An agent that terminates the conversation."""

    _system_message = textwrap.dedent(
        """
        You are an agent that terminates the conversation by just saying 'TERMINATE'.
        """
    )

    def __init__(self, config: Config):
        super().__init__(
            name="termination_agent",
            system_message=self._system_message,
            model_client=ChatCompletionClient.load_component(config.model_client),
        )
