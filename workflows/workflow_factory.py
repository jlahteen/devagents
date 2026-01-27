from monitoring.monitor import MonitorBase
from utils.config import Config
from workflows.workflow_base import WorkflowBase


class WorkflowFactory:
    """Defines a factory for creating workflow instances."""

    @staticmethod
    def create_workflow(workflow_name: str, config: Config, monitor: MonitorBase = None) -> WorkflowBase:
        """Creates a workflow based on a specified workflow name."""

        match workflow_name:
            case "NewApp" | "new-app":
                from workflows.new_app.new_app_workflow import NewAppWorkflow

                return NewAppWorkflow(config=config, monitor=monitor)

            case "ModifyApp" | "modify-app":
                from workflows.modify_app.modify_app_workflow import ModifyAppWorkflow

                return ModifyAppWorkflow(config=config, monitor=monitor)

            case "NewCode" | "new-code":
                from workflows.new_code.new_code_workflow import NewCodeWorkflow

                return NewCodeWorkflow(config=config, monitor=monitor)

            case "ModifyCode" | "modify-code":
                from workflows.modify_code.modify_code_workflow import ModifyCodeWorkflow

                return ModifyCodeWorkflow(config=config, monitor=monitor)

            case "FixBuild" | "fix-build":
                from workflows.fix_build.fix_build_workflow import FixBuildWorkflow

                return FixBuildWorkflow(config=config, monitor=monitor)

            case "FixTests" | "fix-tests":
                from workflows.fix_tests.fix_tests_workflow import FixTestsWorkflow

                return FixTestsWorkflow(config=config, monitor=monitor)

            case _:
                raise ValueError(f"Unknown workflow: '{workflow_name}'")
