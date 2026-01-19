from workflows.app_workflow_base import AppWorkflowBase
from monitoring.monitor import MonitorBase
from utils.config import Config
from utils.constants import WorkflowType


class NewAppWorkflow(AppWorkflowBase):
    """A workflow for creating a new application."""

    def __init__(
        self,
        config: Config,
        monitor: MonitorBase = None,
    ):
        super().__init__(
            config=config,
            workflow_type=WorkflowType.NEW_APP,
            monitor=monitor,
        )
