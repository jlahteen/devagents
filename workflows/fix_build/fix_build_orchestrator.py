from autogen_agentchat.ui import Console

from agents.build_agent import BuildAgent
from workflows.orchestrator_base import OrchestratorBase, OrchestratorContext
from utils.config import Config
from utils.constants import BUILD_AGENT_FAILED, BUILD_AGENT_SUCCESSFUL


class FixBuildOrchestrator(OrchestratorBase):
    """An orchestrator to run a FixBuild scenario."""

    def __init__(self, config: Config, context: OrchestratorContext = None):
        super().__init__(config=config, context=context)
        self._build_agent = BuildAgent(config=config, context=context)

    async def run_team(self, prompt: str) -> None:
        """Runs the team with a given prompt."""

        await Console(self._build_agent.run_stream(task=prompt))
