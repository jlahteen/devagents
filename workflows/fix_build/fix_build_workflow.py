from agents.build_agent import BuildAgent
from workflows.workflow_base import WorkflowBase
from monitoring.monitor import MonitorBase
from utils.config import Config


class FixBuildWorkflow(WorkflowBase):
    """A workflow to ensure an application builds successfully."""

    def __init__(self, config: Config, monitor: MonitorBase = None):
        super().__init__(config=config, monitor=monitor)
        self._build_agent = BuildAgent(config=config, monitor=monitor, on_error_callback=self._add_error)

    async def run(self, prompt: str) -> None:
        """Runs the workflow with a given prompt."""

        await self._build_agent.run_inner_team(prompt=prompt)
