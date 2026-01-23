from agents.test_agent import TestAgent
from monitoring.monitor import MonitorBase
from utils.config import Config
from workflows.workflow_base import WorkflowBase


class FixTestsWorkflow(WorkflowBase):
    """A workflow to ensure all tests pass successfully."""

    def __init__(
        self,
        config: Config,
        monitor: MonitorBase = None,
    ):
        super().__init__(
            config=config,
            monitor=monitor,
        )
        self._test_agent = TestAgent(config=config, monitor=monitor, on_error_callback=self._add_error)

    async def run(self, prompt: str) -> None:
        """Runs the workflow with a given prompt."""

        await self._test_agent.run_inner_team(prompt=prompt)
