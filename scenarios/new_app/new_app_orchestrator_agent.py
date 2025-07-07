import textwrap
from typing import Sequence

from autogen_agentchat.messages import AgentEvent, ChatMessage
from autogen_agentchat.teams import SelectorGroupChat
from autogen_agentchat.ui import Console

from config import Config
from constants import BUILD_AGENT_SUCCESSFUL, SCAFFOLD_AGENT_DONE
from scenarios.orchestrator_agent_base import OrchestratorAgentBase
from utils.misc import over_to


class NewAppOrchestratorAgent(OrchestratorAgentBase):
    """An orchestrator to run a NewApp scenario."""

    _system_message = textwrap.dedent(
        """
        You are an orchestrator agent that manages a team of AI agents to complete a coding task.
        """
    )

    def __init__(
        self,
        config: Config,
        scaffold_agent,
        developer_agent,
        reviewer_agent,
        output_agent,
        build_agent,
        test_agent,
    ):
        super().__init__(
            name="orchestrator_agent",
            system_message=self._system_message,
            config=config,
        )
        self._scaffold_agent = scaffold_agent
        self._developer_agent = developer_agent
        self._reviewer_agent = reviewer_agent
        self._output_agent = output_agent
        self._build_agent = build_agent
        self._test_agent = test_agent

    def select_next_speaker(self, messages: Sequence[AgentEvent | ChatMessage]):
        if len(messages) == 1:
            return over_to(self._scaffold_agent.name)
        elif messages[-1].source == self._scaffold_agent.name:
            if SCAFFOLD_AGENT_DONE in messages[-1].content:
                return over_to(self._developer_agent.name)
            else:
                return over_to(self._scaffold_agent.name)
        elif messages[-1].source == self._developer_agent.name:
            return over_to(self._reviewer_agent.name)
        elif messages[-1].source is self._reviewer_agent.name:
            if self._is_code_approved(messages[-1].content):
                return over_to(self._output_agent.name)
            else:
                return over_to(self._developer_agent.name)
        elif messages[-1].source == self._output_agent.name:
            return over_to(self._build_agent.name)
        elif messages[-1].source == self._build_agent.name:
            if BUILD_AGENT_SUCCESSFUL in messages[-1].content:
                return over_to(self._test_agent.name)
            return over_to(self._termination_agent.name)
        elif messages[-1].source == self._test_agent.name:
            return over_to(self._termination_agent.name)
        elif messages[-1].source == self._termination_agent.name:
            return over_to(self._termination_agent.name)
        else:
            # Raise an error if the source is not recognized
            raise ValueError(f"Unknown message source: {messages[-1].source}")

    async def run_team(self, prompt: str) -> None:
        """Runs the team with a given prompt."""

        self.groupchat = SelectorGroupChat(
            [
                self._scaffold_agent,
                self._developer_agent,
                self._reviewer_agent,
                self._output_agent,
                self._build_agent,
                self._test_agent,
                self._termination_agent,
            ],
            model_client=self._model_client,
            selector_func=self.select_next_speaker,
            max_turns=self._config.max_turns,
            termination_condition=self._termination_condition,
        )
        await Console(self.groupchat.run_stream(task=prompt))
