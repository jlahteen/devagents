from workflows.modify_code.modify_code_orchestrator import ModifyCodeOrchestrator
from workflows.orchestrator_base import OrchestratorBase, OrchestratorContext
from workflows.scenario_base import ScenarioBase
from utils.config import Config


class ModifyCodeScenario(ScenarioBase):
    """A scenario for modifying existing code files."""

    def create_orchestrator(self, config: Config, context: OrchestratorContext = None) -> OrchestratorBase:
        orchestrator = ModifyCodeOrchestrator(config=config, context=context)
        return orchestrator
