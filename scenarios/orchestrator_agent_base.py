import re
from abc import abstractmethod
from dataclasses import dataclass

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.conditions import TextMentionTermination
from autogen_core.models import ChatCompletionClient

from agents.termination_agent import TerminationAgent
from config import Config
from monitoring.monitor import MonitorBase


@dataclass
class OrchestratorAgentContext:
    """
    Defines a context for orchestrator agents. This context includes properties for reporting the execution of the
    orchestrator agent.
    """

    monitor: MonitorBase
    errors: list[Exception]


class OrchestratorAgentBase(AssistantAgent):
    """A base class for orchestrator agents."""

    def __init__(
        self,
        name,
        system_message,
        config: Config,
        context: OrchestratorAgentContext = None,
    ):
        super().__init__(
            name=name,
            system_message=system_message,
            model_client=ChatCompletionClient.load_component(config.model_client),
        )
        self._config: Config = config
        self._context: OrchestratorAgentContext = context
        self._termination_agent = TerminationAgent(config=config)
        self._termination_condition = TextMentionTermination("TERMINATE")

    @abstractmethod
    async def run_team(self, prompt: str):
        """Runs the team with a given prompt."""
        pass

    def _over_to(self, agent_name: str) -> str:
        """Handles the over_to event."""

        if self._context is not None:
            self._context.monitor.set_current_agent(agent_name)
        return agent_name

    def _add_error(self, error: Exception):
        """Adds an error to the orchestrator agent context."""

        if self._context is not None:
            self._context.errors.append(error)

    def _is_code_approved(self, message):
        """Checks whether the code is approved in the given message."""

        # Use a regex to match 'CODE APPROVED' surrounded by any special characters
        pattern = r"[^a-zA-Z0-9]*CODE\sAPPROVED[^a-zA-Z0-9]*"

        # Split the message into lines and get the last line
        last_line = message.strip().split("\n")[-1]

        # Check the pattern against the last line
        return bool(re.fullmatch(pattern, last_line))
