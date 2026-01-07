from scenarios.fix_tests.fix_tests_orchestrator import FixTestsOrchestrator
from scenarios.orchestrator_base import OrchestratorBase, OrchestratorContext
from scenarios.scenario_base import ScenarioBase
from utils.config import Config


class FixTestsScenario(ScenarioBase):
    """A scenario to ensure all tests pass successfully."""

    def create_orchestrator(self, config: Config, context: OrchestratorContext = None) -> OrchestratorBase:
        orchestrator = FixTestsOrchestrator(config=config, context=context)
        return orchestrator
