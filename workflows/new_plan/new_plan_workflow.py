from agent_platform.agent_base import Message
from agent_platform.agent_team import AgentTeam
from agents.architect_agent import ArchitectAgent
from agents.architecture_reviewer_agent import ArchitectureReviewerAgent
from agents.task_analyzer_agent import TaskAnalyzerAgent
from agents.task_planner_agent import TaskPlannerAgent
from monitoring.monitor import MonitorBase
from utils.config import Config
from utils.constants import (
    ARCHITECT_AGENT_DONE,
    ARCHITECT_AGENT_FAILED,
    ARCHITECTURE_REVIEW_RESULT_APPROVED,
    ARCHITECTURE_REVIEW_RESULT_CHANGES_REQUIRED,
    TASK_ANALYZER_AGENT_DONE,
    TASK_PLANNER_AGENT_DONE,
)
from workflows.workflow_base import WorkflowBase


class NewPlanWorkflow(WorkflowBase):
    """A workflow to create an implementation plan based on specifications."""

    def __init__(self, config: Config, monitor: MonitorBase = None):
        """Initializes the workflow with necessary agents."""

        super().__init__(config=config, monitor=monitor)
        self._architect_agent = ArchitectAgent(config=config)
        self._architecture_reviewer_agent = ArchitectureReviewerAgent(config=config)
        self._task_analyzer_agent = TaskAnalyzerAgent(config=config)
        self._task_planner_agent = TaskPlannerAgent(config=config, monitor=monitor, on_error_callback=self._add_error)

    def _select_next_speaker(self, message_count: int, last_message: Message | None):
        """Selects the next speaker based on the message count and last message."""

        if message_count == 1:
            return self._over_to(self._architect_agent.name)
        elif last_message.source == self._architect_agent.name:
            if ARCHITECT_AGENT_DONE in last_message.content:
                return self._over_to(self._architecture_reviewer_agent.name)
            elif ARCHITECT_AGENT_FAILED in last_message.content:
                self._add_error(RuntimeError(ARCHITECT_AGENT_FAILED))
                return self._over_to(self._termination_agent.name)
            else:
                return self._over_to(self._architect_agent.name)
        elif last_message.source == self._architecture_reviewer_agent.name:
            if ARCHITECTURE_REVIEW_RESULT_APPROVED in last_message.content:
                return self._over_to(self._task_analyzer_agent.name)
            elif ARCHITECTURE_REVIEW_RESULT_CHANGES_REQUIRED in last_message.content:
                return self._over_to(self._architect_agent.name)
            else:
                return self._over_to(self._architecture_reviewer_agent.name)
        elif last_message.source == self._task_analyzer_agent.name:
            if TASK_ANALYZER_AGENT_DONE in last_message.content:
                return self._over_to(self._task_planner_agent.name)
            else:
                return self._over_to(self._task_analyzer_agent.name)
        elif last_message.source == self._task_planner_agent.name:
            if TASK_PLANNER_AGENT_DONE in last_message.content:
                return self._over_to(self._termination_agent.name)
            else:
                return self._over_to(self._task_planner_agent.name)
        elif last_message.source == self._termination_agent.name:
            return self._over_to(self._termination_agent.name)
        else:
            raise ValueError(f"Unknown message source: {last_message.source}")

    async def run(self, prompt: str) -> None:
        """Runs the workflow with a given prompt."""

        self._agent_team = AgentTeam(
            agents=[
                self._architect_agent,
                self._architecture_reviewer_agent,
                self._task_analyzer_agent,
                self._task_planner_agent,
                self._termination_agent,
            ],
            config=self._config,
            selector_func=self._select_next_speaker,
            termination_condition=self._termination_condition,
        )
        await self._agent_team.run(prompt=prompt)
