import textwrap

from agent_platform.agent_base import AgentBase
from utils.config import Config


class TerminationAgent(AgentBase):
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
            config=config,
        )
