from autogen_agentchat.agents import SocietyOfMindAgent
from autogen_agentchat.teams import Team
from autogen_core.models import ChatCompletionClient, ChatCompletionContext

from scenarios.orchestrator_agent_base import OrchestratorAgentBase, OrchestratorContext


class InnerTeamAgentBase(SocietyOfMindAgent):
    def __init__(
        self,
        name: str,
        team: Team,
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

    def _over_to(self, agent_name: str):
        """Handles the over_to event."""

        if self._context is not None:
            self._context.monitor.set_current_agent(self.name + "." + agent_name)

    def _add_error(self, error: Exception):
        """Adds an error to the orchestrator context."""

        if self._context is not None:
            self._context.errors.append(error)
