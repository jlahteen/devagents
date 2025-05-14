import textwrap

from autogen_agentchat.ui import Console

from config import Config
from scenarios.orchestrator_agent_base import OrchestratorAgentBase


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
        test_agent,
    ):
        super().__init__(
            name="orchestrator_agent",
            system_message=self._system_message,
            config=config,
        )
        self._test_agent = test_agent

    async def run_team(self, coding_task: str) -> None:
        """Runs the team with a given coding task."""

        await Console(self._test_agent.run_stream(task=coding_task))
