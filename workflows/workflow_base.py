from abc import abstractmethod

from agent_platform.termination import MessageTermination
from agents.termination_agent import TerminationAgent
from monitoring.monitor import MonitorBase
from utils.config import Config


class WorkflowBase:
    """A base class for workflows."""

    def __init__(
        self,
        config: Config,
        monitor: MonitorBase = None,
    ):
        self._config: Config = config
        self._monitor: MonitorBase = monitor
        self._errors: list[Exception] = []
        self._termination_agent = TerminationAgent(config=config)
        self._termination_condition = MessageTermination("TERMINATE")

    @abstractmethod
    async def run(self, prompt: str):
        """Runs the workflow with a given prompt."""
        pass

    @property
    def errors(self) -> list[Exception]:
        """Returns the list of errors encountered during the workflow execution."""
        return self._errors

    def _over_to(self, agent_name: str) -> str:
        """Handles the over_to event."""

        if self._monitor is not None:
            self._monitor.set_current_agent(agent_name)
        return agent_name

    def _add_error(self, error: Exception):
        """Adds an error to the workflow errors list."""

        self._errors.append(error)
