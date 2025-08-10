from autogen_agentchat.agents import SocietyOfMindAgent
from autogen_agentchat.teams import SelectorGroupChat
from autogen_core.models import ChatCompletionClient

from scenarios.orchestrator_agent_base import OrchestratorContext
from utils.autogen import SuccessOrFailureTermination


class InnerTeamAgentBase(SocietyOfMindAgent):
    def __init__(
        self,
        name: str,
        team: SelectorGroupChat,
        model_client: ChatCompletionClient,
        instruction: str,
        response_prompt: str,
        context: OrchestratorContext = None,
    ):
        super().__init__(
            name=name,
            team=team,
            model_client=model_client,
            instruction=instruction,
            response_prompt=response_prompt,
        )
        self._context = context

    def _over_to(self, agent_name: str) -> str:
        """Handles the over_to event."""

        if self._context is not None:
            self._context.monitor.set_current_agent(self.name + "." + agent_name)
        return agent_name

    def _add_error(self, error: Exception):
        """Adds an error to the orchestrator context."""

        if self._context is not None:
            self._context.errors.append(error)

    def _on_failure(self, message: str):
        """Handles the failure event."""

        if self._context is not None:
            self._context.errors.append(RuntimeError(message))

    def _create_termination_condition(self, success_phrase: str, failure_phrase: str):
        """Creates a termination condition for the inner team agent."""

        return SuccessOrFailureTermination(
            success_phrase=success_phrase, failure_phrase=failure_phrase, on_failure_callback=self._on_failure
        )
