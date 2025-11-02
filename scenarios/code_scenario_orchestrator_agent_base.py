import textwrap
from typing import Sequence

from autogen_agentchat.messages import AgentEvent, ChatMessage
from autogen_agentchat.teams import SelectorGroupChat
from autogen_agentchat.ui import Console

from agents.developer_agent import DeveloperAgent
from agents.output_agent import OutputAgent
from agents.reviewer_agent import ReviewerAgent
from scenarios.orchestrator_agent_base import OrchestratorAgentBase, OrchestratorContext
from utils.config import Config
from utils.constants import (
    DEVELOPER_AGENT_DONE,
    OUTPUT_AGENT_DONE,
    REVIEW_RESULT_APPROVED,
    REVIEW_RESULT_CHANGES_REQUIRED,
    ScenarioType,
)


class CodeScenarioOrchestratorAgentBase(OrchestratorAgentBase):
    """A base orchestrator agent to run code level scenarios."""

    _system_message = textwrap.dedent(
        """
        You are an orchestrator agent that manages a team of AI agents to complete a scenario task.
        """
    )

    def __init__(
        self,
        config: Config,
        scenario_type: ScenarioType,
        context: OrchestratorContext = None,
    ):
        super().__init__(
            name="orchestrator_agent",
            system_message=self._system_message,
            config=config,
            context=context,
        )
        self._developer_agent = DeveloperAgent(config=config, scenario_type=scenario_type)
        self._reviewer_agent = ReviewerAgent(config=config, scenario_type=scenario_type)
        self._output_agent = OutputAgent(config=config)

    def _select_next_speaker(self, messages: Sequence[AgentEvent | ChatMessage]):
        if len(messages) == 1:
            return self._over_to(self._developer_agent.name)
        elif messages[-1].source == self._developer_agent.name:
            if DEVELOPER_AGENT_DONE in messages[-1].content:
                return self._over_to(self._reviewer_agent.name)
            else:
                return self._over_to(self._developer_agent.name)
        elif messages[-1].source is self._reviewer_agent.name:
            if REVIEW_RESULT_APPROVED in messages[-1].content:
                return self._over_to(self._output_agent.name)
            elif REVIEW_RESULT_CHANGES_REQUIRED in messages[-1].content:
                return self._over_to(self._developer_agent.name)
            else:
                return self._over_to(self._reviewer_agent.name)
        elif messages[-1].source == self._output_agent.name:
            if OUTPUT_AGENT_DONE in messages[-1].content:
                return self._over_to(self._termination_agent.name)
            else:
                return self._over_to(self._output_agent.name)
        elif messages[-1].source == self._termination_agent.name:
            return self._over_to(self._termination_agent.name)
        else:
            raise ValueError(f"Unknown message source: {messages[-1].source}")

    async def run_team(self, prompt: str) -> None:
        """Runs the team with a given prompt."""

        self.groupchat = SelectorGroupChat(
            [
                self._developer_agent,
                self._reviewer_agent,
                self._output_agent,
                self._termination_agent,
            ],
            model_client=self._model_client,
            selector_func=self._select_next_speaker,
            max_turns=self._config.max_turns,
            termination_condition=self._termination_condition,
        )
        await Console(self.groupchat.run_stream(task=prompt))
