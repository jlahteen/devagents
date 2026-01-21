import datetime
import os

from monitoring.console_monitor_ansi import ConsoleMonitorAnsi
from workflows.workflow_factory import WorkflowFactory
from utils.config import Config
from utils.misc import generate_timestamp, to_os_path
from utils.tee import Tee


class WorkflowResult:
    """Defines the result of a workflow."""

    def __init__(
        self,
        workflow_name: str = None,
        started_at: datetime.datetime = None,
        finished_at: datetime.datetime = None,
        run_id: str = None,
        workspace: str = None,
        errors: list[Exception] = None,
    ):
        """Initializes a new workflow result."""

        self.workflow_name: str = workflow_name
        self.started_at: datetime.datetime = started_at
        self.finished_at: datetime.datetime = finished_at
        self.elapsed: datetime.timedelta = finished_at - started_at if started_at and finished_at else None
        self.run_id: str = run_id
        self.workspace: str = workspace
        self.errors: list[Exception] = errors if errors is not None else []


class WorkflowEngine:
    """An engine for running workflows."""

    async def run_workflow(self, workflow_name: str, prompt: str, workspace: str) -> WorkflowResult:
        """Runs a workflow with a given prompt in the specified workspace."""

        run_id = generate_timestamp()
        started_at = datetime.datetime.now()
        finished_at = None

        try:
            # Validate the workspace
            self._validate_workspace(workspace)

            # Create a Monitor and trace file
            monitor = ConsoleMonitorAnsi()
            trace_file = self._create_trace_file(workspace, run_id)

            # Create a Tee instance
            tee = Tee(monitor, trace_file)

            # Run the workflow
            original_dir = os.getcwd()
            try:
                # Create the workflow
                workflow = WorkflowFactory.create_workflow(
                    workflow_name=workflow_name,
                    config=Config(),
                    monitor=monitor
                )
                os.chdir(workspace)
                await workflow.run(prompt)
            finally:
                os.chdir(original_dir)
                tee.close()
                finished_at = datetime.datetime.now()

            return WorkflowResult(
                workflow_name=workflow_name,
                started_at=started_at,
                finished_at=finished_at,
                run_id=run_id,
                workspace=workspace,
                errors=workflow.errors,
            )

        except Exception as e:
            return WorkflowResult(
                workflow_name=workflow_name,
                started_at=started_at,
                finished_at=finished_at if finished_at else datetime.datetime.now(),
                run_id=run_id,
                workspace=workspace,
                errors=[e],
            )

    def _validate_workspace(self, workspace: str):
        """Validates the workspace path."""

        if not workspace:
            raise ValueError("Workspace is required.")

        if not os.path.exists(workspace):
            raise FileNotFoundError(f"Workspace '{workspace}' does not exist.")

        if not os.path.isdir(workspace):
            raise NotADirectoryError(f"Workspace '{workspace}' is not a directory.")

    def _create_trace_file(self, workspace: str, run_id: str):
        """Creates a trace file for saving the agent conversation."""

        trace_file_dir = to_os_path(workspace + "\\.devagents")
        if not os.path.exists(trace_file_dir):
            os.makedirs(trace_file_dir)
        trace_file_path = to_os_path(trace_file_dir + "\\trace-" + run_id + ".md")
        trace_file = open(trace_file_path, "w", encoding="utf-8")
        return trace_file
