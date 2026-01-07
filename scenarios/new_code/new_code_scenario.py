from scenarios.new_code.new_code_orchestrator import NewCodeOrchestrator
from scenarios.orchestrator_base import OrchestratorBase, OrchestratorContext
from scenarios.scenario_base import ScenarioBase
from utils.config import Config


class NewCodeScenario(ScenarioBase):
    """A scenario for creating new code files."""

    def create_orchestrator(self, config: Config, context: OrchestratorContext = None) -> OrchestratorBase:
        orchestrator = NewCodeOrchestrator(config=config, context=context)
        return orchestrator
