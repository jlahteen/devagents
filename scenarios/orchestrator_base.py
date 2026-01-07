from abc import abstractmethod
from dataclasses import dataclass

from monitoring.monitor import MonitorBase
from utils.config import Config


@dataclass
class OrchestratorContext:
    """
    Defines a context for orchestrators. This context includes properties for reporting the execution of the
    orchestrator agent.
    """

    monitor: MonitorBase
    errors: list[Exception]


class OrchestratorBase:
    """A base class for orchestrators."""

    def __init__(
        self,
        config: Config,
        context: OrchestratorContext = None,
    ):
        self._config: Config = config
        self._context: OrchestratorContext = context

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
        """Adds an error to the orchestrator context."""

        if self._context is not None:
            self._context.errors.append(error)
