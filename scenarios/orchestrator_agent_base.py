import re
from abc import abstractmethod

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.conditions import TextMentionTermination
from autogen_core.models import ChatCompletionClient

from agents.termination_agent import TerminationAgent
from config import Config
from monitoring.monitor import MonitorBase


class OrchestratorAgentBase(AssistantAgent):
    """A base class for orchestrator agents."""

    def __init__(
        self,
        name,
        system_message,
        config: Config,
    ):
        super().__init__(
            name=name,
            system_message=system_message,
            model_client=ChatCompletionClient.load_component(config.model_client),
        )
        self._config = config
        self._termination_agent = TerminationAgent(config=config)
        self._termination_condition = TextMentionTermination("TERMINATE")
        self._monitor: MonitorBase = None

    @abstractmethod
    async def run_team(self, prompt: str):
        """Runs the team with a given prompt."""
        pass

    def set_monitor(self, monitor: MonitorBase):
        """Sets a monitor for the orchestrator agent."""

        self._monitor = monitor

    def _is_code_approved(self, message):
        """Checks whether the code is approved in the given message."""

        # Use a regex to match 'CODE APPROVED' surrounded by any special characters
        pattern = r"[^a-zA-Z0-9]*CODE\sAPPROVED[^a-zA-Z0-9]*"

        # Split the message into lines and get the last line
        last_line = message.strip().split("\n")[-1]

        # Check the pattern against the last line
        return bool(re.fullmatch(pattern, last_line))
