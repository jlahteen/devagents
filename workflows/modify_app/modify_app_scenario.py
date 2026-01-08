from workflows.modify_app.modify_app_orchestrator import ModifyAppOrchestrator
from workflows.orchestrator_base import OrchestratorBase, OrchestratorContext
from workflows.scenario_base import ScenarioBase
from utils.config import Config


class ModifyAppScenario(ScenarioBase):
    """A scenario for modifying an existing application."""

    def create_orchestrator(self, config: Config, context: OrchestratorContext = None) -> OrchestratorBase:
        orchestrator = ModifyAppOrchestrator(config=config, context=context)
        return orchestrator
