from scenarios.fix_build.fix_build_orchestrator import FixBuildOrchestrator
from scenarios.orchestrator_base import OrchestratorBase, OrchestratorContext
from scenarios.scenario_base import ScenarioBase
from utils.config import Config


class FixBuildScenario(ScenarioBase):
    """A scenario to ensure an application builds successfully."""

    def create_orchestrator(self, config: Config, context: OrchestratorContext = None) -> OrchestratorBase:
        orchestrator = FixBuildOrchestrator(config=config, context=context)
        return orchestrator
