import textwrap

from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console

from config import Config
from constants import BUILD_AGENT_FAILED, BUILD_AGENT_SUCCESSFUL
from scenarios.orchestrator_agent_base import OrchestratorAgentBase


class FixBuildErrorsOrchestratorAgent(OrchestratorAgentBase):
    """An orchestrator to run a FixBuildErrors scenario."""

    _system_message = textwrap.dedent(
        """
        You are an orchestrator agent that manages a team of AI agents to complete a coding task.
        """
    )

    def __init__(
        self,
        config: Config,
        build_agent,
    ):
        super().__init__(
            name="orchestrator_agent",
            system_message=self._system_message,
            config=config,
        )
        self._build_agent = build_agent

    async def start_chat(self, coding_request):
        """Starts the chat with the given coding request."""

        termination_condition = TextMentionTermination(BUILD_AGENT_SUCCESSFUL) or TextMentionTermination(
            BUILD_AGENT_FAILED
        )
        groupchat = RoundRobinGroupChat(
            [self._build_agent],
            max_turns=self._config.max_turns,
            termination_condition=termination_condition,
        )
        await Console(groupchat.run_stream(task=coding_request))
