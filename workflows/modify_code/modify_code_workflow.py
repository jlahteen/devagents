from monitoring.monitor import MonitorBase
from utils.config import Config
from utils.constants import WorkflowType
from workflows.code_workflow_base import CodeWorkflowBase


class ModifyCodeWorkflow(CodeWorkflowBase):
    """A workflow for modifying existing code files."""

    def __init__(
        self,
        config: Config,
        monitor: MonitorBase = None,
    ):
        super().__init__(
            config=config,
            workflow_type=WorkflowType.MODIFY_CODE,
            monitor=monitor,
        )
