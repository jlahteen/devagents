from workflows.new_app.new_app_orchestrator import NewAppOrchestrator
from workflows.orchestrator_base import OrchestratorBase, OrchestratorContext
from workflows.scenario_base import ScenarioBase
from utils.config import Config


class NewAppScenario(ScenarioBase):
    """A scenario for creating a new application."""

    def create_orchestrator(self, config: Config, context: OrchestratorContext = None) -> OrchestratorBase:
        orchestrator = NewAppOrchestrator(config=config, context=context)
        return orchestrator
