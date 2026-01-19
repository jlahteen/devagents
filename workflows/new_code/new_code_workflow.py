from workflows.code_workflow_base import CodeWorkflowBase
from monitoring.monitor import MonitorBase
from utils.config import Config
from utils.constants import WorkflowType


class NewCodeWorkflow(CodeWorkflowBase):
    """A workflow for creating new code files."""

    def __init__(
        self,
        config: Config,
        monitor: MonitorBase = None,
    ):
        super().__init__(
            config=config,
            workflow_type=WorkflowType.NEW_CODE,
            monitor=monitor,
        )
