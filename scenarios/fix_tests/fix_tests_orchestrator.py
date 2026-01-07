from autogen_agentchat.ui import Console

from agents.test_agent import TestAgent
from scenarios.orchestrator_base import OrchestratorBase, OrchestratorContext
from utils.config import Config


class FixTestsOrchestrator(OrchestratorBase):
    """An orchestrator to run a FixTests scenario."""

    def __init__(
        self,
        config: Config,
        context: OrchestratorContext = None,
    ):
        super().__init__(
            config=config,
            context=context,
        )
        self._test_agent = TestAgent(config=config, context=context)

    async def run_team(self, prompt: str) -> None:
        """Runs the team with a given prompt."""

        await Console(self._test_agent.run_stream(task=prompt))
