from scenarios.modify_app.modify_app_orchestrator_agent import ModifyAppOrchestratorAgent
from scenarios.orchestrator_agent_base import OrchestratorAgentBase, OrchestratorContext
from scenarios.scenario_base import ScenarioBase
from utils.config import Config


class ModifyAppScenario(ScenarioBase):
    """A scenario for modifying an existing application."""

    def create_orchestrator_agent(self, config: Config, context: OrchestratorContext = None) -> OrchestratorAgentBase:
        # Create an Orchestrator Agent
        orchestrator_agent = ModifyAppOrchestratorAgent(config=config, context=context)
        return orchestrator_agent
