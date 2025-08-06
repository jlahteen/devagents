import datetime
import os

from config import Config
from monitoring.console_monitor_ansi import ConsoleMonitorAnsi
from monitoring.monitor import MonitorBase
from scenarios.orchestrator_agent_base import OrchestratorAgentBase
from scenarios.scenario_base import ScenarioBase
from utils.misc import generate_timestamp, to_os_path
from utils.tee import Tee


class ScenarioTaskResult:
    """Defines the result of a scenario task."""

    def __init__(
        self,
        scenario_name: str = None,
        started_at: datetime.datetime = None,
        finished_at: datetime.datetime = None,
        task_id: str = None,
        workspace: str = None,
        errors: list[Exception] = None,
    ):
        """Initializes a new scenario task result."""

        self.scenario_name: str = scenario_name
        self.started_at: datetime.datetime = started_at
        self.finished_at: datetime.datetime = finished_at
        self.elapsed: datetime.timedelta = finished_at - started_at if started_at and finished_at else None
        self.task_id: str = task_id
        self.workspace: str = workspace
        self.errors: list[Exception] = errors if errors is not None else []


class ScenarioTask:
    """Defines a scenario task."""

    def __init__(self, scenario_name: str, prompt: str, workspace: str):
        """Initializes a new scenario task."""

        self.scenario_name: str = scenario_name
        self._prompt: str = prompt
        self.workspace: str = workspace
        self.id = generate_timestamp()
        self.started_at: datetime.datetime = None
        self.finished_at: datetime.datetime = None
        self._tee: Tee = None
        self._monitor: MonitorBase = None
        self._scenario: ScenarioBase = None
        self._orchestrator_agent: OrchestratorAgentBase = None

    async def run(self) -> ScenarioTaskResult:
        """Runs the scenario task."""

        self.started_at = datetime.datetime.now()

        # Validate the workspace
        self._validate_workspace(self.workspace)

        # Create the scenario
        self._scenario = ScenarioBase.create_scenario(self.scenario_name)

        # Create an orchestrator agent
        self._orchestrator_agent = self._scenario.create_orchestrator_agent(config=Config())

        # Create a Tee instance for monitoring and tracing
        trace_file = self._create_trace_file()
        monitor = ConsoleMonitorAnsi()
        self._tee = Tee(monitor, trace_file)

        # Run the orchestrator agent with the specified prompt
        original_dir = os.getcwd()
        try:
            os.chdir(self.workspace)
            await self._orchestrator_agent.run_team(self._prompt)
        finally:
            os.chdir(original_dir)
            self._tee.close()
            self.finished_at = datetime.datetime.now()

        return ScenarioTaskResult(
            scenario_name=self.scenario_name,
            started_at=self.started_at,
            finished_at=self.finished_at,
            task_id=self.id,
            workspace=self.workspace,
            errors=self._orchestrator_agent.errors if hasattr(self._orchestrator_agent, "errors") else [],
        )

    def _validate_workspace(self, workspace):
        """Validates the workspace path."""

        if not workspace:
            raise ValueError("Workspace is required.")

        if not os.path.exists(workspace):
            raise FileNotFoundError(f"Workspace '{workspace}' does not exist.")

        if not os.path.isdir(workspace):
            raise NotADirectoryError(f"Workspace '{workspace}' is not a directory.")

    def _create_trace_file(self):
        """Creates a trace file for saving the agent conversation."""

        trace_file_dir = to_os_path(self.workspace + "\\.devagents")
        if not os.path.exists(trace_file_dir):
            os.makedirs(trace_file_dir)
        trace_file_path = to_os_path(trace_file_dir + "\\trace-" + self.id + ".md")
        trace_file = open(trace_file_path, "w", encoding="utf-8")
        return trace_file
