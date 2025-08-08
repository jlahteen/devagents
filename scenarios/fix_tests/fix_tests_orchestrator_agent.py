import textwrap

from autogen_agentchat.ui import Console

from agents.test_agent import TestAgent
from config import Config
from scenarios.orchestrator_agent_base import OrchestratorAgentBase, OrchestratorContext


class FixTestsOrchestratorAgent(OrchestratorAgentBase):
    """An orchestrator to run a FixTests scenario."""

    _system_message = textwrap.dedent(
        """
        You are an orchestrator agent that manages a team of AI agents to complete a coding task.
        """
    )

    def __init__(
        self,
        config: Config,
        context: OrchestratorContext = None,
    ):
        super().__init__(
            name="orchestrator_agent",
            system_message=self._system_message,
            config=config,
            context=context,
        )
        self._test_agent = TestAgent(config=config)

    async def run_team(self, prompt: str) -> None:
        """Runs the team with a given prompt."""

        await Console(self._test_agent.run_stream(task=prompt))
