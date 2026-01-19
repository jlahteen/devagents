from agent_platform.agent_base import AgentBase, SpeakerSelectorFunc
from agent_platform.inner_team_agent_base import InnerTeamAgentBase
from agent_platform.termination import SuccessOrFailureTermination
from monitoring.monitor import MonitorBase
from utils.config import Config


class InnerTeamAgent(InnerTeamAgentBase):
    """
    Defines an InnerTeamAgent.
    """

    def __init__(
        self,
        name: str,
        config: Config,
        agents: list[AgentBase],
        speaker_selector: SpeakerSelectorFunc,
        system_message: str,
        response_prompt: str,
        success_phrase: str,
        failure_phrase: str,
        monitor: MonitorBase = None,
        on_error_callback: callable = None,
    ):
        """
        Initialize a new InnerTeamAgent instance.
        """

        self._monitor = monitor
        self._on_error_callback = on_error_callback
        termination_condition = SuccessOrFailureTermination(
            success_phrase=success_phrase,
            failure_phrase=failure_phrase,
            on_failure_callback=self._on_failure,
        )

        super().__init__(
            name=name,
            config=config,
            agents=agents,
            speaker_selector=speaker_selector,
            termination_condition=termination_condition,
            system_message=system_message,
            response_prompt=response_prompt,
        )

    def _over_to(self, agent_name: str) -> str:
        """Handles an over_to event by updating the monitor."""

        if self._monitor is not None:
            self._monitor.set_current_agent(f"{self.name}.{agent_name}")
        return agent_name

    def _add_error(self, error: Exception):
        """Adds an error via a callback to a workflow."""

        if self._on_error_callback is not None:
            self._on_error_callback(error)

    def _on_failure(self, message: str):
        """Handles a failure event by adding an error via a callback."""

        if self._on_error_callback is not None:
            self._on_error_callback(RuntimeError(message))
