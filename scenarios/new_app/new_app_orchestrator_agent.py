import textwrap
from typing import Sequence

from autogen_agentchat.messages import AgentEvent, ChatMessage
from autogen_agentchat.teams import SelectorGroupChat
from autogen_agentchat.ui import Console

from agents.build_agent import BuildAgent
from agents.developer_agent import DeveloperAgent
from agents.output_agent import OutputAgent
from agents.reviewer_agent import ReviewerAgent
from agents.scaffold_agent import ScaffoldAgent
from agents.test_agent import TestAgent
from scenarios.orchestrator_agent_base import OrchestratorAgentBase, OrchestratorContext
from utils.config import Config
from utils.constants import BUILD_AGENT_SUCCESSFUL, SCAFFOLD_AGENT_DONE


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
        context: OrchestratorContext = None,
    ):
        super().__init__(
            name="orchestrator_agent",
            system_message=self._system_message,
            config=config,
            context=context,
        )
        self._scaffold_agent = ScaffoldAgent(config=config)
        self._developer_agent = DeveloperAgent(config=config)
        self._reviewer_agent = ReviewerAgent(config=config)
        self._output_agent = OutputAgent(config=config)
        self._build_agent = BuildAgent(config=config, context=context)
        self._test_agent = TestAgent(config=config, context=context)

    def _select_next_speaker(self, messages: Sequence[AgentEvent | ChatMessage]):
        if len(messages) == 1:
            return self._over_to(self._scaffold_agent.name)
        elif messages[-1].source == self._scaffold_agent.name:
            if SCAFFOLD_AGENT_DONE in messages[-1].content:
                return self._over_to(self._developer_agent.name)
            else:
                return self._over_to(self._scaffold_agent.name)
        elif messages[-1].source == self._developer_agent.name:
            return self._over_to(self._reviewer_agent.name)
        elif messages[-1].source is self._reviewer_agent.name:
            if self._is_code_approved(messages[-1].content):
                return self._over_to(self._output_agent.name)
            else:
                return self._over_to(self._developer_agent.name)
        elif messages[-1].source == self._output_agent.name:
            return self._over_to(self._build_agent.name)
        elif messages[-1].source == self._build_agent.name:
            if BUILD_AGENT_SUCCESSFUL in messages[-1].content:
                return self._over_to(self._test_agent.name)
            return self._over_to(self._termination_agent.name)
        elif messages[-1].source == self._test_agent.name:
            return self._over_to(self._termination_agent.name)
        elif messages[-1].source == self._termination_agent.name:
            return self._over_to(self._termination_agent.name)
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
            selector_func=self._select_next_speaker,
            max_turns=self._config.max_turns,
            termination_condition=self._termination_condition,
        )
        await Console(self.groupchat.run_stream(task=prompt))
