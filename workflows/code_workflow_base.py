import textwrap
from typing import Sequence

from agent_platform.agent_base import Message
from agent_platform.agent_team import AgentTeam
from agents.developer_agent import DeveloperAgent
from agents.output_agent import OutputAgent
from agents.reviewer_agent import ReviewerAgent
from monitoring.monitor import MonitorBase
from workflows.workflow_base import WorkflowBase
from utils.config import Config
from utils.constants import (
    DEVELOPER_AGENT_DONE,
    OUTPUT_AGENT_DONE,
    REVIEW_RESULT_APPROVED,
    REVIEW_RESULT_CHANGES_REQUIRED,
    WorkflowType,
)


class CodeWorkflowBase(WorkflowBase):
    """A base workflow to run code level workflows."""

    def __init__(
        self,
        config: Config,
        workflow_type: WorkflowType,
        monitor: MonitorBase = None,
    ):
        super().__init__(
            config=config,
            monitor=monitor,
        )
        self._developer_agent = DeveloperAgent(config=config, workflow_type=workflow_type)
        self._reviewer_agent = ReviewerAgent(config=config, workflow_type=workflow_type)
        self._output_agent = OutputAgent(config=config)

    def _select_next_speaker(self, message_count: int, last_message: Message | None):
        if message_count == 1:
            return self._over_to(self._developer_agent.name)
        elif last_message.source == self._developer_agent.name:
            if DEVELOPER_AGENT_DONE in last_message.content:
                return self._over_to(self._reviewer_agent.name)
            else:
                return self._over_to(self._developer_agent.name)
        elif last_message.source is self._reviewer_agent.name:
            if REVIEW_RESULT_APPROVED in last_message.content:
                return self._over_to(self._output_agent.name)
            elif REVIEW_RESULT_CHANGES_REQUIRED in last_message.content:
                return self._over_to(self._developer_agent.name)
            else:
                return self._over_to(self._reviewer_agent.name)
        elif last_message.source == self._output_agent.name:
            if OUTPUT_AGENT_DONE in last_message.content:
                return self._over_to(self._termination_agent.name)
            else:
                return self._over_to(self._output_agent.name)
        elif last_message.source == self._termination_agent.name:
            return self._over_to(self._termination_agent.name)
        else:
            raise ValueError(f"Unknown message source: {last_message.source}")

    async def run(self, prompt: str) -> None:
        """Runs the workflow with a given prompt."""

        self._agent_team = AgentTeam(
            agents=[
                self._developer_agent,
                self._reviewer_agent,
                self._output_agent,
                self._termination_agent,
            ],
            config=self._config,
            selector_func=self._select_next_speaker,
            termination_condition=self._termination_condition,
        )
        await self._agent_team.run(prompt=prompt)
