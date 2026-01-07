from scenarios.app_scenario_orchestrator_base import AppScenarioOrchestratorBase
from scenarios.orchestrator_base import OrchestratorContext
from utils.config import Config
from utils.constants import ScenarioType


class ModifyAppOrchestrator(AppScenarioOrchestratorBase):
    """An orchestrator to run a ModifyApp scenario."""

    def __init__(
        self,
        config: Config,
        context: OrchestratorContext = None,
    ):
        super().__init__(
            config=config,
            scenario_type=ScenarioType.MODIFY_APP,
            context=context,
        )
