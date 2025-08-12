import textwrap

from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console

from agents.build_agent import BuildAgent
from constants import BUILD_AGENT_FAILED, BUILD_AGENT_SUCCESSFUL
from scenarios.orchestrator_agent_base import OrchestratorAgentBase, OrchestratorContext
from utils.config import Config


class FixBuildOrchestratorAgent(OrchestratorAgentBase):
    """An orchestrator to run a FixBuild scenario."""

    _system_message = textwrap.dedent(
        """
        You are an orchestrator agent that manages a team of AI agents to complete a coding task.
        """
    )

    def __init__(self, config: Config, context: OrchestratorContext = None):
        super().__init__(name="orchestrator_agent", system_message=self._system_message, config=config, context=context)
        self._build_agent = BuildAgent(config=config, context=context)

    async def run_team(self, prompt: str) -> None:
        """Runs the team with a given prompt."""

        await Console(self._build_agent.run_stream(task=prompt))
