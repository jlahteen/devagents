from workflows.app_scenario_orchestrator_base import AppScenarioOrchestratorBase
from workflows.orchestrator_base import OrchestratorContext
from utils.config import Config
from utils.constants import ScenarioType


class NewAppOrchestrator(AppScenarioOrchestratorBase):
    """An orchestrator to run a NewApp scenario."""

    def __init__(
        self,
        config: Config,
        context: OrchestratorContext = None,
    ):
        super().__init__(
            config=config,
            scenario_type=ScenarioType.NEW_APP,
            context=context,
        )
