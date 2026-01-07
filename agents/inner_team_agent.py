from agent_platform.agent_base import AgentBase, SpeakerSelectorFunc
from agent_platform.inner_team_agent_base import InnerTeamAgentBase
from agent_platform.termination import SuccessOrFailureTermination
from scenarios.orchestrator_base import OrchestratorContext
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
        context: OrchestratorContext = None,
    ):
        """
        Initialize a new InnerTeamAgent instance.
        """

        self._context = context
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
        """Handles the over_to event by updating the monitor."""

        if self._context is not None and hasattr(self._context, "monitor"):
            self._context.monitor.set_current_agent(f"{self.name}.{agent_name}")
        return agent_name

    def _add_error(self, error: Exception):
        """Adds an error to the orchestrator context."""

        if self._context is not None and hasattr(self._context, "errors"):
            self._context.errors.append(error)

    def _on_failure(self, message: str):
        """Handles the failure event by adding an error to context."""

        if self._context is not None and hasattr(self._context, "errors"):
            self._context.errors.append(RuntimeError(message))
